// SPDX-License-Identifier: MIT
#pragma once

#include <math.h>
#include "tinyusdz.hh"
#include "stream-reader.hh"

#include "ascii-parser.hh"

namespace tinyusdz {

namespace usda {

struct USDAReaderConfig {
  bool allow_unknown_prims{true};
  bool allow_unknown_shader{true};
  bool allow_unknown_apiSchema{true};
};

///
/// Test if input file is USDA format.
///
bool IsUSDA(const std::string &filename, size_t max_filesize = 0);

class USDAReader {
 public:
  struct ParseState {
    int64_t loc{-1};  // byte location in StreamReder
  };

  USDAReader() = delete;
  USDAReader(tinyusdz::StreamReader *sr);

  USDAReader(const USDAReader &rhs) = delete;
  USDAReader(USDAReader &&rhs) = delete;

  ~USDAReader();


  ///
  /// Base filesystem directory to search asset files.
  ///
  void SetBaseDir(const std::string &base_dir);

  ///
  /// Set reader option
  ///
  void set_reader_config(const USDAReaderConfig &config);

  ///
  /// Get reader option
  ///
  const USDAReaderConfig get_reader_config() const; // NOTE: Not returning reference to avoid static memory allocation.

  ///
  /// Check if header data is USDA
  ///
  bool CheckHeader();

  ///
  /// Reader entry point
  ///
  bool Read(LoadState state = LoadState::Toplevel);

#if 0
  ///
  ///
  ///
  std::string GetDefaultPrimName() const;

  ///
  /// Get parsed toplevel "def" nodes(GPrim)
  ///
  std::vector<GPrim> GetGPrims();
#endif

  ///
  /// Get error message(when `Parse` failed)
  ///
  std::string GetError();

  ///
  /// Get warning message(warnings in `Parse`)
  ///
  std::string GetWarning();

  ///
  /// Get read USD scene data as Layer
  /// Must be called after `Read`
  ///
  bool GetAsLayer(Layer *layer);

  ///
  /// Reconstruct Stage from loaded USD scene data.
  /// Must be called after `Read`
  ///
  bool ReconstructStage();

  ///
  /// Get as stage(scene graph). Must call `ReconstructStage` beforehand.
  ///
  const Stage& GetStage() const;

 private:
#if defined(TINYUSDZ_DISABLE_MODULE_USDA_READER)
  Stage *_empty_stage{nullptr};
#else
  class Impl;
  Impl *_impl{nullptr};
#endif

};

} // namespace usda

} // namespace tinyusdz
