{
  src,
  nixpkgs,
}: let
  supported = ["python38" "python39" "python310" "python311"];
  version = let
    file_str = builtins.readFile "${src}/fa_purity/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
  in
    builtins.elemAt match 0;
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).project // {inherit version;};
  publish = import ./publish {
    inherit nixpkgs;
  };
  build_pkg = {
    lib,
    python_pkgs,
  }:
    import ./pkg {
      inherit lib metadata python_pkgs src;
    };
  build_for = selected_python: let
    lib = {
      buildEnv = nixpkgs."${selected_python}".buildEnv.override;
      buildPythonPackage = nixpkgs."${selected_python}".pkgs.buildPythonPackage;
      fetchPypi = nixpkgs.python3Packages.fetchPypi;
    };
    python_pkgs = import ./deps lib nixpkgs selected_python;
    self_pkgs = build_pkg {
      inherit lib python_pkgs;
    };
    checks = import ./ci/check.nix {self_pkg = self_pkgs.pkg;};
  in {
    check = checks;
    env = self_pkgs.env;
    pkg = self_pkgs.pkg;
  };

  pkgs = builtins.listToAttrs (map
    (name: {
      inherit name;
      value = build_for name;
    })
    supported);
in
  pkgs
  // {
    inherit publish build_pkg;
  }
