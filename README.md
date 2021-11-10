# The Vertnet Traits Database Project ![CI](https://github.com/rafelafrance/traiter_vertnet/workflows/CI/badge.svg)

# All right, what's this all about then?
**Challenge**: Extract trait information from unstructured or semi-structured natural history field notations. That is, if I'm given text like:

 ```
 This rather large female specimen is 12 lbs 7 oz and 3 feet 7 inches in total length.
 ```
I should be able to extract:

 - sex = female
 - body mass = 5,641 g
 - total length = 1,092 mm

 Of course, this is a rather straight-forward example. Natural history/museum notations are highly idiosyncratic and may use various shorthand notations. Here are just a few examples of how total length measurements appear:

 - Total Length: 15.7 cm
 - 15.7cm T.L.
 - 157-60-20-19=21g
 - SVL 157 mm
 - standard length: 157-215mm
 - t.l. = 2 feet 3.1 - 4.5 inches
 - As well as measurements embedded in prose like: "Snout vent lengths range anywhere from 16 to 23 cm."
 - We flag ambiguous measurements like: "length: 12.0". This may be a total length measurement or another length measurement.
 - We also flag numeric measurements without units like: "total length = 120". The units may or may not be the default millimeters.
 - etc.

Values from controlled vocabularies are also extracted.
 - These values sometimes have a signifier like "Life Stage: Adult"
 - And other times we see a value on its own like "Adult" without the signifier.

# File processing

In general, I take a CSV file as input (almost always from VerNet) and process each record in the CSV file. There are fields that are targeted for parsing (finding traits) and other fields that are just carried through to the output as is. The following VerNet fields are usually targets for parsing.

- `dynamicproperties`
- `fieldnotes`
- `occurrenceremarks`
- `reproductivecondition` - We only want sex traits from this field.

So we are taking one CSV file and (usually) producing another CSV file. The output will have traits added to it. A simplified example of the output of parsing body mass from the `dynamicproperties` field.

binomial|body_mass.1.is_shorthand|location|body_mass.1.units_inferred|body_mass.1.value|dynamicproperties
---------|------------------------|--------|--------------------------|-----------------|-----------------
Abrothrix olivaceus| |dynamicproperties|False|20|sex=male ; total length=165 mm; weight=20 g
Akodon olivaceus|True|dynamicproperties|False|24.5|{"measurements":"182.5-84.5-24.5-17=24.5g"}
Abrothrix olivaceus| |dynamicproperties|True|17.5|; BodyMass: 17.5
Abrothrix olivaceus| |dynamicproperties|False|19|sex=male ; total length=140 mm; weight=19 g;

# Column trait column headers (trait.1.field)

There are two or three parts to a trait column header field. We either have "trait.n.field" or just "trait.field". The number part (if it exists) is a tiebreaker that indicates which extracted trait we are working for that row. For instance, we may have multiple body masses, one from the dynamicproperties and one from the fieldnotes. Or, we may have multiple body masses from the same field. It's just a way to disambiguate them.

The first part is described in [Traits extracted](#Traits-extracted) and the third part is described in [Trait column header fields](#Trait-column-header-fields).

# Traits extracted

As mentioned above, this is the first part of the trait column header. For example the "body_mass" in **body_mass**.1.value

   - `body_mass`: grams
   - `ear_length`: millimeters
   - `embryo_count`: integer
   - `embryo_length`: millimeters
   - `forearm_length`: millimeters 
   - `hind_foot_length`: millimeters
   - `lactation_state`: text
   - `life_stage`: text
   - `nipple_count`: integer
   - `nipple_state`: text
   - `nipple_enlarged`: text
   - `ovaries_size`: millimeters
   - `ovaries_state`: text
   - `placental_scar_count`: integer
   - `placental_scar_state`: text
   - `pregnancy_state`: text
   - `scrotal_state`: text
   - `sex`: text
   - `tail_length`: millimeters
   - `testes_size`: millimeters
   - `testes_state`: text
   - `thumb_length`: millimeters
   - `tibia_length`: millimeters
   - `total_length`: millimeters
   - `tragus_length`: millimeters
   - `vagina_state`: text

# Trait column header fields

 This is the last part of the trait column header the for example the "value" in: body_mass. There are a few different flags/values:

   - `value` is either a measurement normalized to millimeters or grams or a controlled vocabulary value. This depends on the trait being extracted.
   - `is_shorthand` = did the trait measurement come from a shorthand notation like "182.5-84.5-24.5-17=24.5g".
   - `units_inferred` indicate if the units for the trait were missing from the input data and were guessed.
   - `ambiguous_key` indicates when we guessed at a key value. For instance, "weight" usually indicates a body mass, but it may represent any other mass.
   - `estimated_value`: Some traits are noted as estimated in the input data itself, so we carry the flag through to the output.
   - `side`: Was the trait taken from the left/right side also indicated as side 1/2.
   - `units`: Are the original units in the trait.
   - `dimension`: Is this a length or width measurement.
   - `question`: Was the trait flagged with a question mark in the input? If so, we carry this through to the output.
   - `includes`: Does the hind-foot measurement include the claw?

# Parsing strategy

This implementation uses a technique that I call **"Stacked Regular Expressions"**. The concept is very simple, we build tokens in one step and in the next two steps we use those tokens to reduce combinations to other tokens or productions.

1. Tokenize the text.
2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.
3. Convert sequences of tokens into the final productions.
* Postprocessing of the extracted information is performed by the caller.

All steps use regular expressions. Step 1 uses them on raw text like any other regular expression but the other two steps use them on the token stream. The regular expressions on the token stream look and behave just like normal regular expressions, but they are adjusted to work on tokens & not text. I.e. steps 2 & 3 use a domain specific language (DSL) for the token-level regular expressions.

Note that I am trying to extract data from patterns of text and not parse a formal language. Most importantly, I don't need to worry about recursive structures. Pattern recognition is a common technique in **Natural Language Processing, Information Extraction**.

Another point to note, is that we want to parse gigabytes (or terabytes) of data in a "reasonable" amount of time. So speed may not be the primary concern but having fast turnaround is still important. The development of parsers that use this module tends to be iterative.

**The drawback of this approach is that it tends to have a significantly higher precision than recall.**

### 1. Tokenize the text
Replace text with tokens. We use regular expressions to create a token stream from the raw text. During this process, any text that is not captured by a token regex is removed from the token stream, i.e. noise is removed from the text.
   
The following regular expressions will return a sequence of tokens with the name as one of (animal, color, etc.) and what the regular expression matches as the value of the token. 

```python
keyword('animal', r' dogs? | cats? ')
keyword('color', r' brown | black | white | tan | gr [ae] y')
keyword('age', r' adult | puppy | younger | older ')
keyword('fur', r' fur | hair ' )
fragment('and', r' [&] | \b and \b ')
```

`keyword` and `fragment` are methods for adding token regular expressions to the parser. The `keyword` surrounds a pattern with `\b` word-separator character class and the `fragment` method does not.

Tokens are scanned in order so if two tokens would read the same sequence of characters the first one wins. This can be very useful when you have pattern conflicts.

Given these rules and the following text: `The specimen is an older dog with tan and gray fur,` Will produce the following tokens:
- {age: older}
- {animal: dog}
- {color: tan}
- {and: and}
- {color: gray}

Notice that there are no tokens for any of the spaces, any of the words in "The specimen is a", or the final `,` comma. We have removed the "noise". This turns out to be very helpful with simplifying the parsers. 

### 2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.

Replace tokens with other tokens. Use a Domain Specific Language (DSL) to capture sets of tokens that may be combined into a single token. This simplification step is often repeated so simplifications may be built up step-wise.

```python
grouper('color_set', ' color and color ')
```

Continuing the example above the three tokens:
- {color: tan}
- {and: and}
- {color: gray}

Are replaced with the single token:
- {color_set: 'tan and gray', 'color': ["tan", "gray"]}

Note that this rule will match any pair of colors linked by the word "and". Also note that the original information is preserved. So the new "color_set" token also has a color list of `["tan", "gray"]`.
 
### 3. Convert sequences of tokens into the final productions
Replace tokens with the final tokens. Everything except the final tokens are removed. This final stream of tokens is what the client code processes.

Here is a rule for recognizing fur color.

```python
def fur_color(token):
    """Process the token for fur color."""
    trait = Trait(start=token.start, end=token.end, color=token.color)
    # Other processing may happen here.
    return trait

producer(fur_color, r' ( color | mixed_color ) fur ')
```

Keeping with the example above we get the following information:
- {fur_color: 'tan and gray fur', 'color': ["brown", "gray"]}

 Combined token data is preserved just like it is in step 2. We will have the fur_color data but also the color list of `["tan", "gray"]`.

### The domain specific language (DSL).

Token names are just regular expression group names and follow the same rules. All rules are case-insensitive and use the verbose regular expression syntax.

The `grouper`s and `producer`s (steps 2 & 3 not in step 1). Use a simple domain specific language based on regular expressions. In fact, they are just slightly modified regular expressions. The only conceptual difference is that a token in a grouper or producer regular expression can be treated as if it is a single character. So you can do things like:
```python
keyword('modifier', 'dark | light')
grouper('color_phrase', ' modifier? color ')
```
The "modifier" token is treated as a single unit. But also note that you still have to group multiple tokens if you want to do something like:
```python
keyword('modifier', 'dark | light')
grouper('color_phrase', ' modifier? ( color and )? color ')
```
Here "color and" is two tokens and must be grouped as you would have to group letters in a normal regular expression.

# Postprocessing of the output traits

Note that there are actually two phases of postprocessing.
1. As the final stage of processing tokens after the `producer`s are run. This handles the output of the producer on a per-trait basis. Some things handled here are:
   1. Normalize all measurements to millimeters and grams. For instance, we convert any measurements given  inches to millimeters.
   2. Normalization of controlled vocabulary fields like life stage or sex. There may be abbreviations or phrase that mean roughly the same thing, like "F" and "Fem" for "female", these are normalized.
   3. Rejecting of productions that are actually not traits. For instance, if we have a production for an ear length like `E 20` and it is near another notation like `N 32` then it is much more likely to be a longitude and not an ear measurement, and is therefore rejected.
   4. Etc.
2. At per data record level of process all traits for a record. Some examples include:
   1. (Optional) Some researchers only want one of each trait for any data record. For instance if there are two total length measurements in the `dynamicproperties` field and two total lengths in the `fieldnotes` field then I may either drop all but the first measurement or just report the extrema (min/max) of all the measurements.
   2. If the sex is clearly a male or female then we will remove measurements for the wrong sex from `reproductivecondition` fields. If a testes measurement is in a record for a female then it is removed.
   3. When there are too many annotation for a particular trait, then I'll remove that particular trait for that record. I have seen over twenty sex annotations for a single record, in that case we remove the sex notation for that record but keep the other traits.
   4. Remove trait lists that have become empty and then remove records that also become empty.
   5. Etc.

# Install

You will need to have Python3 installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user --requirement traiter/requirements.txt
```
  
# Run
I typically use an arguments file when running this process. So a run looks similar to:
```
cd /my/path/to/traiter
./traiter.py @args/all_mammals.args
```
Look in the `args` directory for argument examples.

# Tests
Having a test suite is absolutely critical. The strategy I use is every new pattern gets its own test. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. Most test are targeted at the traits being produced and not at smaller units of code.

You can run the tests like so:
```
cd /my/path/to/traiter
python -m unittest discover
```
