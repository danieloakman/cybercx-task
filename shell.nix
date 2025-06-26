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
    # swig
    glibc
    glib.dev
    # libffi
    # ffmpeg
    # libsmf
    # libGL
    # libz
    # libzip
    # libgcc
    zlib
    # pango
    # fontconfig
    # libstdcxx5
    # opencv
    cmake
    # pixman
    # cairo
    # libjpeg
    # giflib
    # librsvg
    # cairomm_1_16

    # Needed for prisma:
    # openssl
    # prisma-engines 
  ];
  # ++ (with pkgs.xorg; [
  #   libX11
  #   libXext
  #   libSM
  # ]);
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
