# Changelog

## [Unreleased]

## [1.2.5] - 2022-03-15

### Changed

- MacOS and Windows support temporarily disabled, since OpenFST python extension
  is platform dependant and pre-built for Linux only.

## [1.2.4] - 2021-06-14

### Added

- MANIFEST.in file to specify to-be-packaged data files.

### Fixed

- Ensures that OpenFST Python wrapper gets included in the release package.

## [1.2.3] - 2021-06-14

### Fixed

- Analyzer can now be built using Python 3.9.

## [1.2.2] - 2020-09-08

### Changed

- Faster decomposition of human-readable analysis into analysis protobufs, by
  caching the affix decomposition logic.

## [1.2.1] - 2020-04-09

### Fixed

- Surface form generation of proper nouns using morphological analysis that
  doesn't have proper features.

## [1.2.0] - 2020-04-01

### Added

- An API module to generate Turkish word forms from morphological analyses.

### Changed

- Moved functions of analyze API module, which are used to build FSTs from
  symbols, compose FSTs and to extract parses from FSTs into fst API. They
  are now public functions.

## [1.1.0] - 2020-03-22

### Added

- An API module to validate structural well-formedness of analysis protobufs.
- An API module to construct human-readable analysis strings from analysis
  protobufs.

### Changed

- Refactored functions which read and extract Turkish morphological analyzer
  FST into the fst API module.

### Fixed

- Enclosed messages defined in analysis.proto in turkish\_morphology namespace.

## [1.0.0] - 2020-03-15

### Added

- Initial release of the Turkish Morphology together with a simple Python API
  to morpholgically analyze word forms, and to parse human-readable analysis
  strings into protobuf messages.

[unreleased]: https://github.com/google-research/turkish-morphology/compare/v1.2.5...HEAD
[1.2.5]: https://github.com/google-research/turkish-morphology/compare/v1.2.4...v1.2.5
[1.2.4]: https://github.com/google-research/turkish-morphology/compare/v1.2.3...v1.2.4
[1.2.3]: https://github.com/google-research/turkish-morphology/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/google-research/turkish-morphology/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/google-research/turkish-morphology/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/google-research/turkish-morphology/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/google-research/turkish-morphology/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/google-research/turkish-morphology/releases/tag/v1.0.0
