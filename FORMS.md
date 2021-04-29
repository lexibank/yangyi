## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `(';', '/', ',')`
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `('烂饭', '-', '---', '三只', '他是白族')`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[('  腮帮  po²¹mɯ̠⁵⁵ɣɯ⁵⁵', ''), (' (借汉方言 )', ''), (' H3 F1 09', ''), (' (新黄村、松桂等)', ''), (' (lua³⁵ = 很)', ''), (' 0 VW', ''), (' H2 ', ''), ('H4 2Z', ''), (' (= not clean)', ''), ('F1', ''), ('①', ''), ('H4 F8 PV', ''), ('H4 F9 UB', ''), ('；a²²ja³³', ''), ('②', ''), ('F2', ''), (' H3 F1 09', ''), ('H4 F4 AZ', ''), (' H3 F6 IK', ''), ('，', ''), ('（无生命）', ''), ('男性称呼弟弟 pʰo²¹mo³³女性称呼弟弟：', ''), (' F3 6G', ''), ('H4 F2 2Z', ''), ('H4 F4 AZ', ''), (' H3 F1 09', ''), ('五天后', ''), ('三只', ''), ('舅母：', ''), ('H3', ''), (' H2 F1', ''), ('他是白族', ''), ('婶婶', ''), ('④', ''), ('③', ''), ('舅母', ''), (' 2nd syllable sandhi', ''), ('男用', ''), ('̪', ''), ('̩', ''), ('6G', ''), ('借汉', ''), (' F10 WV', ''), (' 腮帮 po²¹mɯ̠⁵⁵ɣɯ⁵⁵', ''), ('09', ''), (' 2nd syll', ''), ('??', ''), ('男用', ''), ('[ɛ²¹no³³]', 'ɛ²¹no³³'), ('[kɑ̠¹³]', 'kɑ̠¹³'), ('女用', ''), ('男性称呼弟弟', ''), (' F10 WV', ''), ('H4 F4 AZ', ''), ('，', ''), ('H4 F8 PV', ''), (' *m-b', ''), ('没录', ''), (' H3 F6 IK', ''), ('H4 F2 2Z', ''), (' 腮帮  po²¹mɯ̠⁵⁵ɣɯ⁵⁵', ''), (' ', '_'), ('\u3000', '_'), ('___', '_'), ('__', '_')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `True`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')