# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `Session` class `__contains__` method
- `Session` class `mask_message` method
- `Session` class `unmask_message` method
- `Session` class `masks` attribute
### Changed
- `inference_time` parameter added to `Response` class
- `README.md` updated
- Test system modified
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


[Unreleased]: https://github.com/openscilab/memor/compare/v0.3...dev
[0.3]: https://github.com/openscilab/memor/compare/v0.2...v0.3
[0.2]: https://github.com/openscilab/memor/compare/v0.1...v0.2
[0.1]: https://github.com/openscilab/memor/compare/6594313...v0.1