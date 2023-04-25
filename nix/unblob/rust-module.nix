{ lib, stdenv, pname, version, craneLib, rustPlatform, nix-filter, python, setuptools, setuptools-rust, libiconv ? stdenv.isDarwin }:

let
  unblob-rust-src = nix-filter {
    root = ../../.;
    include = [
      "pyproject.toml"
      "setup.py"
      "Cargo.toml"
      "Cargo.lock"
      "rust"
    ];
  };
  cargoArtifacts = craneLib.buildDepsOnly {
    inherit version;
    pname = "${pname}-rust";
    src = unblob-rust-src;

    buildInputs = [ python ];
  };

in
craneLib.mkCargoDerivation {
  inherit version;
  pname = "${pname}-rust";
  src = unblob-rust-src;

  buildInputs = [ python setuptools setuptools-rust ] ++ lib.optional stdenv.isDarwin [
    libiconv
  ];
  nativeBuildInputs = with rustPlatform; [
    rust.cargo
    rust.rustc
  ];
  inherit cargoArtifacts;
  UNBLOB_BUILD_RUST_EXTENSION = "1";
  buildPhaseCargoCommand = ''
    mkdir unblob
    touch unblob/__init__.py
    python setup.py bdist
  '';
  installPhaseCommand = ''
    mkdir -p $out
    cp -a build/lib.*/* $out
  '';
}
