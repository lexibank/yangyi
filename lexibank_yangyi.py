from pathlib import Path

import attr
from clldutils.misc import slug
from pylexibank import FormSpec
from pylexibank import Language, Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


@attr.s
class CustomLanguage(Language):
    Location = attr.ib(default=None)
    Source = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")
    SubGroup = attr.ib(default="Yi")
    NameInData = attr.ib(default=None)
    Number = attr.ib(default=None)


@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    id = "yangyi"
    dir = Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(missing_data=("烂饭", "-", "---"), first_form_only=True)

    def cmd_makecldf(self, args):
        # read raw data for later addition
        raw_entries = self.raw_dir.read_csv("data.tsv", delimiter="\t")
        raw_entry_dicts = []
        for row in raw_entries[2:]:
            raw_entry_dicts += [{k.strip(): v for k, v in zip(raw_entries[0],
                row)}]
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="NameInData")

        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
                Chinese_Gloss=concept.attributes["chinese"],
            )
            concepts[concept.attributes["number_in_source"]] = idx

        for row in progressbar(raw_entry_dicts, desc="cldfify", total=len(raw_entries)):
            number = row["Yang 2015 #"]
            for language, lid in languages.items():
                entry = row[language]
                if entry.strip():
                    args.writer.add_forms_from_value(
                            Language_ID=lid,
                            Parameter_ID=concepts[number],
                            Value=entry,
                            Source=""
                            )

