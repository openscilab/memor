# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `Session` class `search` method
### Changed
- Validation bug fixed in `update_messages` method in `Session` class
- Validation bug fixed in `from_json` method in `PromptTemplate`, `Response`, `Prompt`, and `Session` classes\
- `AI_STUDIO` render format modified
- Test system modified
## [0.6] - 2025-05-05
### Added
- `Response` class `id` property
- `Prompt` class `id` property
- `Response` class `regenerate_id` method
- `Prompt` class `regenerate_id` method
- `Session` class `render_counter` method
- `Session` class `remove_message_by_index` and `remove_message_by_id` methods
- `Session` class `get_message_by_index`, `get_message_by_id` and `get_message` methods
- `LLMModel` enum
- `AI_STUDIO` render format
### Changed
- Test system modified
- Modification handling centralized via `_mark_modified` method
- `Session` class `remove_message` method modified
## [0.5] - 2025-04-16
### Added
- `Session` class `check_render` method
- `Session` class `clear_messages` method
- `Prompt` class `check_render` method
- `Session` class `estimate_tokens` method
- `Prompt` class `estimate_tokens` method
- `Response` class `estimate_tokens` method
- `universal_tokens_estimator` function
- `openai_tokens_estimator_gpt_3_5` function
- `openai_tokens_estimator_gpt_4` function
### Changed
- `init_check` parameter added to `Prompt` class
- `init_check` parameter added to `Session` class
- Test system modified
- `Python 3.6` support dropped
- `README.md` updated
## [0.4] - 2025-03-17
### Added
- `Session` class `__contains__` method
- `Session` class `__getitem__` method
- `Session` class `mask_message` method
- `Session` class `unmask_message` method
- `Session` class `masks` attribute
- `Response` class `__len__` method
- `Prompt` class `__len__` method
### Changed
- `inference_time` parameter added to `Response` class
- `README.md` updated
- Test system modified
- Python typing features added to all modules
- `Prompt` class default values updated
- `Response` class default values updated
## [0.3] - 2025-03-08
### Added
- `Session` class `__len__` method
- `Session` class `__iter__` method
- `Session` class `__add__` and `__radd__` methods
### Changed
- `tokens` parameter added to `Prompt` class
- `tokens` parameter added to `Response` class
- `tokens` parameter added to preset templates
- `Prompt` class modified
- `Response` class modified
- `PromptTemplate` class modified
## [0.2] - 2025-03-01
### Added
- `Session` class
### Changed
- `Prompt` class modified
- `Response` class modified
- `PromptTemplate` class modified
- `README.md` updated
- Test system modified
## [0.1] - 2025-02-12
### Added
- `Prompt` class
- `Response` class
- `PromptTemplate` class
- `PresetPromptTemplate` class


[Unreleased]: https://github.com/openscilab/memor/compare/v0.6...dev
[0.6]: https://github.com/openscilab/memor/compare/v0.5...v0.6
[0.5]: https://github.com/openscilab/memor/compare/v0.4...v0.5
[0.4]: https://github.com/openscilab/memor/compare/v0.3...v0.4
[0.3]: https://github.com/openscilab/memor/compare/v0.2...v0.3
[0.2]: https://github.com/openscilab/memor/compare/v0.1...v0.2
[0.1]: https://github.com/openscilab/memor/compare/6594313...v0.1