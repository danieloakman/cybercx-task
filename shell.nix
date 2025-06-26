{ pkgs ? import <nixpkgs> {} }:

(pkgs.mkShell {
  name = "CyberCX-Task-Shell";
  packages = with pkgs; [
    python312
    (python312.withPackages (ps: with ps; [
      pip
      virtualenv
      venvShellHook
    ]))
    stdenv.cc.cc
    glibc
    glib.dev
    zlib
    cmake
  ];
  buildInputs = with pkgs; [
    pkg-config
  ];
  shellHook = ''
    VENV=".venv"
    if [ ! -d "$VENV" ]; then
      python -m venv $VENV
    fi
    source ./$VENV/bin/activate
    export SHELL=${pkgs.zsh}/bin/zsh
    exec $SHELL
  '';
})
