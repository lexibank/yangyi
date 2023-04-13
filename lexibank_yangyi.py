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
    form_spec = FormSpec(missing_data=("烂饭", "-", "---", "三只", '他是白族'), 
            replacements=[
                ("  腮帮  po²¹mɯ̠⁵⁵ɣɯ⁵⁵", ""),
                (" (借汉方言 )", ""),
                (" H3 F1 09", ""),
                (" (新黄村、松桂等)", ""),
                (" (lua³⁵ = 很)", ""),
                (" 0 VW", ""),
                (" H2 ", ""),
                ("H4 2Z", ""),
                (" (= not clean)", ""),
                ("F1", ""), ("①", ""), ("H4 F8 PV", ""), ("H4 F9 UB", ""),
                ("；a²²ja³³", ""),
                ("②", ""),
                ("F2", ""), (" H3 F1 09", ""), ("H4 F4 AZ", ""),
                (" H3 F6 IK", ""), ("，", ""), ("（无生命）", ""),
                ("男性称呼弟弟 pʰo²¹mo³³女性称呼弟弟：", ""),
                (" F3 6G", ""), ("H4 F2 2Z", ""), ("H4 F4 AZ", ""),
                (" H3 F1 09", ""), ("五天后", ""), ("三只", ""),
                ("舅母：", ""),
                ("H3", ""), (" H2 F1", ""), ("他是白族", ""), ("婶婶", ""), 
                ("④", ""), ("③", ""), ("舅母", ""),
                (" 2nd syllable sandhi", ""), ("男用", ""), ("\u032a", ""),
                ("\u0329", ""),
                ("6G", ""), ("借汉", ""), (" F10 WV", ""), (" 腮帮 po²¹mɯ̠⁵⁵ɣɯ⁵⁵", ""),
                ("09", ""),
                (" 2nd syll", ""), ("??", ""),
                ("男用", ""),
                ("[ɛ²¹no³³]", "ɛ²¹no³³"),
                ("[kɑ̠¹³]", "kɑ̠¹³"),
                ("女用", ""),
                ("男性称呼弟弟", ""),
                (" F10 WV", ""),
                ("H4 F4 AZ", ""),
                ("，", ""),
                ("H4 F8 PV", ""),
                (" *m-b", ""),
                ("没录", ""),
                (" H3 F6 IK", ""),
                ("H4 F2 2Z", ""),
                (" 腮帮  po²¹mɯ̠⁵⁵ɣɯ⁵⁵", ""),
                (" ", "_"),
                ("　", "_"),
                ("___", "_"),
                ("__", "_"),
                ],
            first_form_only=True)

    def cmd_makecldf(self, args):
        # read raw data for later addition
        raw_entries = self.raw_dir.read_csv("data.tsv", delimiter="\t")
        raw_entry_dicts = []
        for row in raw_entries[2:]:
            raw_entry_dicts += [{k.strip(): v for k, v in zip(raw_entries[0],
                row)}]
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="NameInData")
        sources = {language["NameInData"]: language["Source"] for language in
                self.languages}

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

        dups = set()
        for row in progressbar(raw_entry_dicts, desc="cldfify", total=len(raw_entries)):
            number = row["Yang 2015 #"]
            for language, lid in languages.items():
                entry = row[language]
                if entry.strip():
                    if (language, entry) in dups:
                        pass
                    else:
                        args.writer.add_forms_from_value(
                                Language_ID=lid,
                                Parameter_ID=concepts[number],
                                Value=entry,
                                Source=sources[language]
                                )
                        dups.add((language, entry))

