"""Write the lib output to an HTML file."""

from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from vertnet.writers.base_writer import BaseWriter


class HtmlWriter(BaseWriter):
    """Write the lib output to an HTML file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.started = None
        self.rows = None

    def __enter__(self):
        """Start the report."""
        self.started = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
        self.rows = []

    def __exit__(self, exc_type, exc_value, traceback):
        """End the report."""
        env = Environment(
            loader=FileSystemLoader("./pylib/writers/templates"), autoescape=True
        )
        args = {
            k: v
            for k, v in vars(self.args).items()
            if k in ("as_is", "extra_field", "search_field", "trait")
        }
        template = env.get_template("html_writer.html").render(
            now=self.started,
            as_is=sorted({f for fds in self.args.as_is.values() for f in fds}),
            args=args,
            rows=self.rows,
        )
        self.args.output_file.write(template)
        self.args.output_file.close()

    def write(self, raw_record, parsed_record):
        """Output a row to the file."""
        for trait, parses in parsed_record.items():
            parsed_record[trait] = [x.__dict__ for x in parses]

        self.rows.append({"raw": raw_record, "parsed": parsed_record})
