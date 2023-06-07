{ lib
, buildPythonPackage
, fetchPypi
, python3
, click
, cstruct
, lzallright
}:

buildPythonPackage rec {
  pname = "jefferson";
  version = "0.4.5";
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-+cPOzzO3bCQAu8LrbjUJ5S/SR5OFitOYLIu5L9t/q+k=";
  };

  nativeBuildInputs = with python3.pkgs; [
    poetry-core
  ];

  propagatedBuildInputs = [
    click
    cstruct
    lzallright
  ];

  pythonImportsCheck = [ "jefferson" ];

}
