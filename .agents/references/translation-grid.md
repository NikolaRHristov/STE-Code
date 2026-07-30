# Translation Worker Grid — 9 Locales

> Source: `ste-code/` and `SCE/` pipeline output
> Target: `translations/<locale>/` per locale
> Workers: ~81 workers across ~27 batches (3 per batch)
> Status: Placeholder only — no translation content yet

## File Inventory (per locale, ~60 files)

### Artifacts (6 files)

| # | Source | Target (per locale) |
|---|--------|---------------------|
| 1 | `ste-code/artifacts/ste-code-distilled-system-prompt.txt` | `translations/<locale>/artifacts/ste-code-distilled-system-prompt.txt` |
| 2 | `ste-code/artifacts/ste-code-self-reading-manual.txt` | `translations/<locale>/artifacts/ste-code-self-reading-manual.txt` |
| 3 | `ste-code/artifacts/ste-code-extraction-methodology.txt` | `translations/<locale>/artifacts/ste-code-extraction-methodology.txt` |
| 4 | `ste-code/artifacts/ste-code-example-turn.txt` | `translations/<locale>/artifacts/ste-code-example-turn.txt` |
| 5 | `ste-code/artifacts/ste-code-deployment-guide.txt` | `translations/<locale>/artifacts/ste-code-deployment-guide.txt` |
| 6 | `ste-code/artifacts/ste-code-readme.md` | `translations/<locale>/artifacts/ste-code-readme.md` |

### System Prompts (4 files)

| # | Source | Target (per locale) |
|---|--------|---------------------|
| 1 | `SCE/narratives/system-prompts/ste-code-micro.md` | `translations/<locale>/system-prompts/ste-code-micro.txt` |
| 2 | `SCE/narratives/system-prompts/ste-code-full.md` | `translations/<locale>/system-prompts/ste-code-full.txt` |
| 3 | `SCE/narratives/system-prompts/ste-code-agentic.md` | `translations/<locale>/system-prompts/ste-code-agentic.txt` |
| 4 | `SCE/narratives/system-prompts/ste-code-developer.md` | `translations/<locale>/system-prompts/ste-code-developer.txt` |

### Dictionary (3 JSON files)

| # | Source | Target (per locale) |
|---|--------|---------------------|
| 1 | `SCE/data/vocabulary/approved-verbs.json` | `translations/<locale>/dictionary/approved-verbs.json` |
| 2 | `SCE/data/vocabulary/approved-adjectives.json` | `translations/<locale>/dictionary/approved-adjectives.json` |
| 3 | `SCE/core/categories/synonym-table.json` | `translations/<locale>/dictionary/synonym-table.json` |

### Adapted Rules (~55 files)

All files from `ste-code/adapted/a-*.md` → `translations/<locale>/adapted/a-*.md`

### SCE Core Rules (~55 files)

All files from `SCE/core/rules/rule-*.md` → `translations/<locale>/rules/rule-*.md`

### Per-Locale README (1 file)

`translations/<locale>/README.md` — locale metadata, status, contribution notes

## Batch Map

Each batch = 3 workers. Workers are named `trNNN`. Files are grouped by category to keep workers focused.

### Batch Group A: zh-CN (Chinese Simplified) — ~60 files, ~20 batches

```
Batch A01: tr001 (artifacts 1-3),     tr002 (artifacts 4-6),     tr003 (system-prompts 1-3)
Batch A02: tr004 (system-prompt 4),   tr005 (dict 1-2),          tr006 (dict 3)
Batch A03: tr007 (adapted 1-5),       tr008 (adapted 6-10),      tr009 (adapted 11-15)
Batch A04: tr010 (adapted 16-20),     tr011 (adapted 21-25),     tr012 (adapted 26-30)
Batch A05: tr013 (adapted 31-35),     tr014 (adapted 36-40),     tr015 (adapted 41-45)
Batch A06: tr016 (adapted 46-50),     tr017 (adapted 51-55),     tr018 (adapted 56-57)
Batch A07: tr019 (rules 1-5),         tr020 (rules 6-10),        tr021 (rules 11-15)
Batch A08: tr022 (rules 16-20),       tr023 (rules 21-25),       tr024 (rules 26-30)
Batch A09: tr025 (rules 31-35),       tr026 (rules 36-40),       tr027 (rules 41-45)
Batch A10: tr028 (rules 46-50),       tr029 (rules 51-55),       tr030 (README)
```

### Batch Group B: ja (Japanese) — ~60 files, ~10 batches

```
Batch B01: tr031 (artifacts 1-3),     tr032 (artifacts 4-6),     tr033 (system-prompts 1-3)
Batch B02: tr034 (system-prompt 4),   tr035 (dict 1-2),          tr036 (dict 3)
Batch B03: tr037 (adapted 1-5),       tr038 (adapted 6-10),      tr039 (adapted 11-15)
Batch B04: tr040 (adapted 16-20),     tr041 (adapted 21-25),     tr042 (adapted 26-30)
Batch B05: tr043 (adapted 31-35),     tr044 (adapted 36-40),     tr045 (adapted 41-45)
Batch B06: tr046 (adapted 46-50),     tr047 (adapted 51-55),     tr048 (adapted 56-57)
Batch B07: tr049 (rules 1-5),         tr050 (rules 6-10),        tr051 (rules 11-15)
Batch B08: tr052 (rules 16-20),       tr053 (rules 21-25),       tr054 (rules 26-30)
Batch B09: tr055 (rules 31-35),       tr056 (rules 36-40),       tr057 (rules 41-45)
Batch B10: tr058 (rules 46-50),       tr059 (rules 51-55),       tr060 (README)
```

### Batch Group C: ko (Korean) — ~60 files, ~10 batches

```
Batch C01: tr061 (artifacts 1-3),     tr062 (artifacts 4-6),     tr063 (system-prompts 1-3)
Batch C02: tr064 (system-prompt 4),   tr065 (dict 1-2),          tr066 (dict 3)
Batch C03: tr067 (adapted 1-5),       tr068 (adapted 6-10),      tr069 (adapted 11-15)
Batch C04: tr070 (adapted 16-20),     tr071 (adapted 21-25),     tr072 (adapted 26-30)
Batch C05: tr073 (adapted 31-35),     tr074 (adapted 36-40),     tr075 (adapted 41-45)
Batch C06: tr076 (adapted 46-50),     tr077 (adapted 51-55),     tr078 (adapted 56-57)
Batch C07: tr079 (rules 1-5),         tr080 (rules 6-10),        tr081 (rules 11-15)
Batch C08: tr082 (rules 16-20),       tr083 (rules 21-25),       tr084 (rules 26-30)
Batch C09: tr085 (rules 31-35),       tr086 (rules 36-40),       tr087 (rules 41-45)
Batch C10: tr088 (rules 46-50),       tr089 (rules 51-55),       tr090 (README)
```

### Batch Group D: es (Spanish) — ~60 files, ~10 batches

```
Batch D01: tr091 (artifacts 1-3),     tr092 (artifacts 4-6),     tr093 (system-prompts 1-3)
Batch D02: tr094 (system-prompt 4),   tr095 (dict 1-2),          tr096 (dict 3)
Batch D03: tr097 (adapted 1-5),       tr098 (adapted 6-10),      tr099 (adapted 11-15)
Batch D04: tr100 (adapted 16-20),     tr101 (adapted 21-25),     tr102 (adapted 26-30)
Batch D05: tr103 (adapted 31-35),     tr104 (adapted 36-40),     tr105 (adapted 41-45)
Batch D06: tr106 (adapted 46-50),     tr107 (adapted 51-55),     tr108 (adapted 56-57)
Batch D07: tr109 (rules 1-5),         tr110 (rules 6-10),        tr111 (rules 11-15)
Batch D08: tr112 (rules 16-20),       tr113 (rules 21-25),       tr114 (rules 26-30)
Batch D09: tr115 (rules 31-35),       tr116 (rules 36-40),       tr117 (rules 41-45)
Batch D10: tr118 (rules 46-50),       tr119 (rules 51-55),       tr120 (README)
```

### Batch Group E: fr (French) — ~60 files, ~10 batches

```
Batch E01: tr121 (artifacts 1-3),     tr122 (artifacts 4-6),     tr123 (system-prompts 1-3)
Batch E02: tr124 (system-prompt 4),   tr125 (dict 1-2),          tr126 (dict 3)
Batch E03: tr127 (adapted 1-5),       tr128 (adapted 6-10),      tr129 (adapted 11-15)
Batch E04: tr130 (adapted 16-20),     tr131 (adapted 21-25),     tr132 (adapted 26-30)
Batch E05: tr133 (adapted 31-35),     tr134 (adapted 36-40),     tr135 (adapted 41-45)
Batch E06: tr136 (adapted 46-50),     tr137 (adapted 51-55),     tr138 (adapted 56-57)
Batch E07: tr139 (rules 1-5),         tr140 (rules 6-10),        tr141 (rules 11-15)
Batch E08: tr142 (rules 16-20),       tr143 (rules 21-25),       tr144 (rules 26-30)
Batch E09: tr145 (rules 31-35),       tr146 (rules 36-40),       tr147 (rules 41-45)
Batch E10: tr148 (rules 46-50),       tr149 (rules 51-55),       tr150 (README)
```

### Batch Group F: de (German) — ~60 files, ~10 batches

```
Batch F01: tr151 (artifacts 1-3),     tr152 (artifacts 4-6),     tr153 (system-prompts 1-3)
Batch F02: tr154 (system-prompt 4),   tr155 (dict 1-2),          tr156 (dict 3)
Batch F03: tr157 (adapted 1-5),       tr158 (adapted 6-10),      tr159 (adapted 11-15)
Batch F04: tr160 (adapted 16-20),     tr161 (adapted 21-25),     tr162 (adapted 26-30)
Batch F05: tr163 (adapted 31-35),     tr164 (adapted 36-40),     tr165 (adapted 41-45)
Batch F06: tr166 (adapted 46-50),     tr167 (adapted 51-55),     tr168 (adapted 56-57)
Batch F07: tr169 (rules 1-5),         tr170 (rules 6-10),        tr171 (rules 11-15)
Batch F08: tr172 (rules 16-20),       tr173 (rules 21-25),       tr174 (rules 26-30)
Batch F09: tr175 (rules 31-35),       tr176 (rules 36-40),       tr177 (rules 41-45)
Batch F10: tr178 (rules 46-50),       tr179 (rules 51-55),       tr180 (README)
```

### Batch Group G: pt-BR (Portuguese Brazil) — ~60 files, ~10 batches

```
Batch G01: tr181 (artifacts 1-3),     tr182 (artifacts 4-6),     tr183 (system-prompts 1-3)
Batch G02: tr184 (system-prompt 4),   tr185 (dict 1-2),          tr186 (dict 3)
Batch G03: tr187 (adapted 1-5),       tr188 (adapted 6-10),      tr189 (adapted 11-15)
Batch G04: tr190 (adapted 16-20),     tr191 (adapted 21-25),     tr192 (adapted 26-30)
Batch G05: tr193 (adapted 31-35),     tr194 (adapted 36-40),     tr195 (adapted 41-45)
Batch G06: tr196 (adapted 46-50),     tr197 (adapted 51-55),     tr198 (adapted 56-57)
Batch G07: tr199 (rules 1-5),         tr200 (rules 6-10),        tr201 (rules 11-15)
Batch G08: tr202 (rules 16-20),       tr203 (rules 21-25),       tr204 (rules 26-30)
Batch G09: tr205 (rules 31-35),       tr206 (rules 36-40),       tr207 (rules 41-45)
Batch G10: tr208 (rules 46-50),       tr209 (rules 51-55),       tr210 (README)
```

### Batch Group H: ru (Russian) — ~60 files, ~10 batches

```
Batch H01: tr211 (artifacts 1-3),     tr212 (artifacts 4-6),     tr213 (system-prompts 1-3)
Batch H02: tr214 (system-prompt 4),   tr215 (dict 1-2),          tr216 (dict 3)
Batch H03: tr217 (adapted 1-5),       tr218 (adapted 6-10),      tr219 (adapted 11-15)
Batch H04: tr220 (adapted 16-20),     tr221 (adapted 21-25),     tr222 (adapted 26-30)
Batch H05: tr223 (adapted 31-35),     tr224 (adapted 36-40),     tr225 (adapted 41-45)
Batch H06: tr226 (adapted 46-50),     tr227 (adapted 51-55),     tr228 (adapted 56-57)
Batch H07: tr229 (rules 1-5),         tr230 (rules 6-10),        tr231 (rules 11-15)
Batch H08: tr232 (rules 16-20),       tr233 (rules 21-25),       tr234 (rules 26-30)
Batch H09: tr235 (rules 31-35),       tr236 (rules 36-40),       tr237 (rules 41-45)
Batch H10: tr238 (rules 46-50),       tr239 (rules 51-55),       tr240 (README)
```

### Batch Group I: ar (Arabic) — ~60 files, ~10 batches

```
Batch I01: tr241 (artifacts 1-3),     tr242 (artifacts 4-6),     tr243 (system-prompts 1-3)
Batch I02: tr244 (system-prompt 4),   tr245 (dict 1-2),          tr246 (dict 3)
Batch I03: tr247 (adapted 1-5),       tr248 (adapted 6-10),      tr249 (adapted 11-15)
Batch I04: tr250 (adapted 16-20),     tr251 (adapted 21-25),     tr252 (adapted 26-30)
Batch I05: tr253 (adapted 31-35),     tr254 (adapted 36-40),     tr255 (adapted 41-45)
Batch I06: tr256 (adapted 46-50),     tr257 (adapted 51-55),     tr258 (adapted 56-57)
Batch I07: tr259 (rules 1-5),         tr260 (rules 6-10),        tr261 (rules 11-15)
Batch I08: tr262 (rules 16-20),       tr263 (rules 21-25),       tr264 (rules 26-30)
Batch I09: tr265 (rules 31-35),       tr266 (rules 36-40),       tr267 (rules 41-45)
Batch I10: tr268 (rules 46-50),       tr269 (rules 51-55),       tr270 (README)
```

## Summary

| Locale | Language | Worker Range | Batches | Files |
|--------|----------|-------------|---------|-------|
| zh-CN | Chinese (Simplified) | tr001-tr030 | 10 | ~60 |
| ja | Japanese | tr031-tr060 | 10 | ~60 |
| ko | Korean | tr061-tr090 | 10 | ~60 |
| es | Spanish | tr091-tr120 | 10 | ~60 |
| fr | French | tr121-tr150 | 10 | ~60 |
| de | German | tr151-tr180 | 10 | ~60 |
| pt-BR | Portuguese (Brazil) | tr181-tr210 | 10 | ~60 |
| ru | Russian | tr211-tr240 | 10 | ~60 |
| ar | Arabic | tr241-tr270 | 10 | ~60 |
| **Total** | **9 locales** | **tr001-tr270** | **90** | **~540** |
