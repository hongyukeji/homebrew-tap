class Polysub < Formula
  desc "Turn any video into subtitles in any language with local or cloud models"
  homepage "https://github.com/hongyukeji/polysub"
  url "https://github.com/hongyukeji/polysub/releases/download/v0.3.1/polysub-0.3.1-macos-arm64.zip"
  version "0.3.1"
  sha256 "50676e87dae36cbc8673da74122aeadca49b280def4ac46573b3799060071cb5"
  license "MIT"

  livecheck do
    url :stable
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :ventura

  # The app is a prebuilt, ad-hoc signed bundle. Homebrew rewrites library load paths of
  # Mach-O files it installs, which would break that signature, so the bundle is kept
  # zipped in libexec during install and unpacked afterwards, untouched.
  def install
    system "ditto", "-c", "-k", "--keepParent", "PolySub.app", "PolySub.zip"
    libexec.install "PolySub.zip"
    prefix.install "THIRD_PARTY_NOTICES.md"
    (bin/"polysub").write <<~SH
      #!/bin/bash
      exec "#{opt_prefix}/PolySub.app/Contents/MacOS/PolySub" "$@"
    SH
    chmod 0755, bin/"polysub"
  end

  post_install_steps do
    run "/usr/bin/ditto", args: ["-x", "-k", "{{libexec}}/PolySub.zip", "{{prefix}}"], writable_paths: ["{{prefix}}"]
  end

  def caveats
    <<~EOS
      Copy the app to /Applications (run it again after `brew upgrade polysub`):
        polysub install

      Or open it in place:
        open #{opt_prefix}/PolySub.app
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/polysub --version")
    system "codesign", "--verify", "--deep", "--strict", prefix/"PolySub.app"
  end
end
