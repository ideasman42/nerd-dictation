{ srcs ? import ./nix/sources.nix
, big-model ? false
}:
let
  pkgs = import srcs.nixpkgs { };

  enModelSmall = pkgs.fetchzip {
    url = "https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip";
    sha256 = "1rl65n2maayggnzi811x6zingkd1ny2z7p0fvcbfaprbz5khz2h8";
  };
  enModelLGraph = pkgs.fetchzip {
    url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip";
    sha256 = "1dl9sf36mn8l3bcxni4qwrv52hwsfmcm9j08km7iz2vhaiz5wn0r";
  };

  enModel =
    if big-model
    then enModelLGraph
    else enModelSmall;

  py-vosk = pkgs.python3Packages.buildPythonPackage rec {
    pname = "vosk";
    version = "0.3.43";
    VOSK_MODEL_PATH = "${enModelSmall}";
    format = "wheel";
    # This package name is weird and can't be found using the simple route.
    # vosk-0.3.43-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl
    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      format = "wheel";
      python = "py3";
      dist = "py3";
      abi = "none";
      platform = "manylinux_2_12_x86_64.manylinux2010_x86_64";
      sha256 = "0v22acm96r3g3ymnka7f6zbsy0xbjriirpnncyj26w4i5m9df299";
    };
    propagatedBuildInputs = with pkgs.python3Packages; [
      requests
      srt
      tqdm
      websockets
    ] ++ [
      pkgs.stdenv.cc.cc.lib
    ];
  };

  nerd-drv = pkgs.callPackage ./. {
    inherit enModel py-vosk;
    python3 = pkgs.python3.withPackages (_: [ py-vosk ]);
  };
in
pkgs.mkShell {
  packages = [ nerd-drv ];
  shellHook = ''
    export VOSK_MODEL_EN=${enModel}
  '';
}
