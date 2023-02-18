inputs: final: prev:

{
  gnustep = prev.callPackage ./nix/gnustep { inherit (prev) gnustep; };
  sasquatch = prev.callPackage ./nix/sasquatch { inherit (prev) squashfsTools; src = inputs.sasquatch; };
  mkPoetryApp = prev.callPackage ./nix/poetry { };
  unblobPython = prev.callPackage ./nix/python { inherit (inputs) pyperscan; };
  unblob = final.unblobPython.pkgs.callPackage ./. { };
  craneLib = inputs.crane.lib.${final.system};
}
