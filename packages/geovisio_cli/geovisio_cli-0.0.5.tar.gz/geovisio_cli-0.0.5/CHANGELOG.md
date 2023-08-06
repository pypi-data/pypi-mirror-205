# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.0.5] - 2023-04-27

### Fixed
- Add a timeout to avoid `requests` module to hang forever if API is not responding


## [0.0.4] - 2023-04-14

### Changed
- Changed the `--path` option of the `geovisio upload` command to a positional argument since it seems more ergonomic. So now `geovisio upload --api-url <some_url> --path <some dir>` is replaced by `geovisio upload --api-url <some_url> <some dir>` (or `geovisio upload <some dir> --api-url <some_url>` since the parameters order is not relevant)
- Improve some error messages

## [0.0.3] - 2023-04-12

### Added
- A new `--is-blurred` flag is available on upload command to inform API that it doesn't need to blur pictures


## [0.0.2] - 2023-04-07

### Fixed
- Pictures were not sorted in alphabetical or numeric order
- Add a `--wait` flag to the upload command to wait for geovisio to have processed all pictures
- Add a `geovisio collection-status` command, to get the status of a collection


## [0.0.1] - 2023-03-14

### Added
- Basic scripts for uploading pictures to a GeoVisio API


[Unreleased]: https://gitlab.com/geovisio/cli/-/compare/0.0.5...main
[0.0.5]: https://gitlab.com/geovisio/cli/-/compare/0.0.4...0.0.5
[0.0.4]: https://gitlab.com/geovisio/cli/-/compare/0.0.3...0.0.4
[0.0.3]: https://gitlab.com/geovisio/cli/-/compare/0.0.2...0.0.3
[0.0.2]: https://gitlab.com/geovisio/cli/-/compare/0.0.1...0.0.2
[0.0.1]: https://gitlab.com/PanierAvide/geovisio/-/commits/0.0.1
