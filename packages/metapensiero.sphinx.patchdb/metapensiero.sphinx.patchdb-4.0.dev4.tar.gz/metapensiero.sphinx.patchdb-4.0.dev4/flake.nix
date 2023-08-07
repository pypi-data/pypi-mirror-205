# -*- coding: utf-8 -*-
# :Project:   PatchDB — Development environment
# :Created:   dom 26 giu 2022, 11:48:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023 Lele Gaifax
#

{
  description = "metapensiero.sphinx.patchdb";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) flip zipLists;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # List of supported Python versions, see also Makefile
        snakes = flip map [ "310" "311"]
          (ver: rec { name = "python${ver}"; value = builtins.getAttr name pkgs;});

        mkPatchDBPkg = python:
          let
            # Current nixpkgs carries sqlparse 0.4.3
            sqlparse' = python.pkgs.sqlparse.overridePythonAttrs (old: rec {
              version = "0.4.4";
              src = python.pkgs.fetchPypi {
                pname = "sqlparse";
                inherit version;
                hash = "sha256-1EYYPoS4NJ+jBh8P5/BsqUumW0JpRv/r5uPoKVMyQgw=";
              };
              format = "pyproject";
              buildInputs = [ python.pkgs.flitBuildHook ];
            });
          in
            python.pkgs.buildPythonPackage rec {
              name = "patchdb";
              src = getSource "patchdb" ./.;
              propagatedBuildInputs = [
                sqlparse'
              ] ++ (with python.pkgs; [
                enlighten
              ]);
              format = "pyproject";
              nativeBuildInputs = [ python.pkgs.pdm-pep517 ];
              doCheck = false;
            };

        patchDBPkgs = flip map snakes
          (py: {
            name = "patchdb-${py.name}";
            value = mkPatchDBPkg py.value;
          });

        patchDBApps = flip map (zipLists snakes patchDBPkgs)
          (combo:
            let
              python = combo.fst.value;
              name = combo.snd.name;
              patchdb = combo.snd.value;
            in {
              inherit name;
              value = {
                type = "app";
                program = "${python.pkgs.toPythonApplication patchdb}/bin/patchdb";};
            });

        mkTestShell = python:
          let
            patchdb = mkPatchDBPkg python;
          in
            pkgs.mkShell {
              name = "Test Python ${python.version}";
              packages = [
                python
                patchdb
              ] ++ (with pkgs; [
                just
                postgresql_15
                yq-go
              ]) ++ (with python.pkgs; [
                docutils
                psycopg
                pytest
                sphinx
              ]);

              LANG="C";
            };

        testShells = flip map snakes
          (py: {
            name = "test-${py.name}";
            value = mkTestShell py.value;
          });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              bump2version
              gnumake
              just
              postgresql_15
              python3
              twine
              yq-go
            ] ++ (with pkgs.python3Packages; [
              babel
              build
              tomli
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        } // builtins.listToAttrs testShells;

        packages = builtins.listToAttrs patchDBPkgs;
        apps = builtins.listToAttrs patchDBApps;
      });
}
