import re
import zipfile


def test_source_is_valid(build):
    assert build.validate() == []


def test_build_is_reproducible(build, tmp_path, monkeypatch):
    monkeypatch.setattr(build, "DIST", tmp_path / "a")
    first = [p.read_bytes() for p in build.build()]
    monkeypatch.setattr(build, "DIST", tmp_path / "b")
    second = [p.read_bytes() for p in build.build()]
    assert first == second


def test_full_zip_matches_source_tree(build, tmp_path, monkeypatch):
    monkeypatch.setattr(build, "DIST", tmp_path)
    full = build.build()[0]
    with zipfile.ZipFile(full) as z:
        names = z.namelist()
        for name in names:
            assert name.startswith("ui-studio/") and ".." not in name and not name.startswith("/")
            info = z.getinfo(name)
            mode = info.external_attr >> 16
            assert not (mode & 0o111) or name.endswith("/"), f"{name} is marked executable"
        files = {n for n in names if not n.endswith("/")}
        expected = {"ui-studio/" + p.relative_to(build.SKILL_DIR).as_posix() for p in build.source_files()}
        assert files == expected
        for p in build.source_files():
            data = z.read("ui-studio/" + p.relative_to(build.SKILL_DIR).as_posix())
            assert data == p.read_bytes().replace(b"\r\n", b"\n")


def test_single_file_build_inlines_every_reference(build):
    text = build.single_file_skill()
    assert "references/" not in text
    headings = re.findall(r"^## Appendix ([A-F])\. ", text, re.M)
    assert headings == list("ABCDEF")
    for name, _ in build.APPENDICES:
        first_rule = (build.SKILL_DIR / "references" / name).read_text(encoding="utf-8").splitlines()[2]
        assert first_rule.strip() in text


def test_sha256sums_lists_both_zips(build, tmp_path, monkeypatch):
    monkeypatch.setattr(build, "DIST", tmp_path)
    build.build()
    lines = (tmp_path / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert [line.split()[1] for line in lines] == ["ui-studio.zip", "ui-studio-single-file.zip"]
    for line in lines:
        digest, name = line.split()
        assert digest == build.sha256(tmp_path / name)


def test_validate_catches_missing_reference(build, monkeypatch):
    monkeypatch.setattr(build, "APPENDICES", build.APPENDICES + [("missing.md", "Missing")])
    assert any("missing.md" in p for p in build.validate())
