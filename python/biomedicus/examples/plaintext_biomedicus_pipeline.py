# Copyright 2019 Regents of the University of Minnesota.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from argparse import ArgumentParser
from pathlib import Path

from nlpnewt import EventsClient, Event, Pipeline, RemoteProcessor, LocalProcessor, Document
from nlpnewt.io.serialization import get_serializer, SerializationProcessor


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("input_directory", metavar="INPUT_DIR")
    parser.add_argument("output_directory", metavar="OUTPUT_DIR")
    parser.add_argument("--events")
    parser.add_argument("--tagger")
    parser.add_argument("--sentences")
    args = parser.parse_args(args)

    input_dir = Path(args.input_directory)
    with EventsClient(address=args.events) as client, Pipeline(
            RemoteProcessor('biomedicus-sentences', address=args.sentences),
            RemoteProcessor('biomedicus-tnt-tagger', address=args.tagger),
            LocalProcessor(SerializationProcessor(get_serializer('json'),
                                                  output_dir=args.output_directory),
                           component_id='serialize',
                           client=client)
    ) as pipeline:
        for path in input_dir.glob("**/*.txt"):
            print("READING FILE:", str(path))
            with path.open('r') as f:
                contents = f.read()
            with Event(event_id=path.stem, client=client) as event:
                document = Document("plaintext", contents)
                event.add_document(document)
                pipeline.run(document)

        pipeline.print_times()


if __name__ == '__main__':
    main()