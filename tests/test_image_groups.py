"""image_groups：Fig./Figure、MinerU <details> 与多图一注解析。"""

import unittest
from pathlib import Path

from paper_extractor.preprocess.image_groups import (
    figure_number_from_caption,
    parse_markdown_text,
    starts_figure_caption_line,
)


class ImageGroupsParseTest(unittest.TestCase):
    def test_starts_figure_caption_line_variants(self) -> None:
        self.assertTrue(starts_figure_caption_line("Figure 1. Stress–strain curves."))
        self.assertTrue(starts_figure_caption_line("Fig. 1. Yield stress"))
        self.assertTrue(starts_figure_caption_line("Fig 2 Engineering curves"))
        self.assertTrue(starts_figure_caption_line("**Figure 1.** Caption here."))
        self.assertTrue(starts_figure_caption_line("### Fig. 3. Microstructure"))
        self.assertFalse(starts_figure_caption_line("The results are shown in Fig. 1 below."))

    def test_figure_number_from_caption(self) -> None:
        self.assertEqual(figure_number_from_caption("Fig. 2. Engineering stress"), "2")
        self.assertEqual(figure_number_from_caption("Figure 10. Results"), "10")

    def test_mineru_details_two_images_one_fig_caption(self) -> None:
        md = """# Paper title

# Abstract

Short abstract here.

# 1. Intro

Text.

![](images/a.jpg)

<details>
<summary>bar</summary>

| x | y |
|---|---|
| 1 | 2 |
</details>

![](images/b.jpg)

<details>
<summary>bar</summary>

| u | v |
|---|---|
| 3 | 4 |
</details>

Fig. 1. Yield stress and hardness (a) and (b).

More body.
"""
        groups = parse_markdown_text(md)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["image_paths"], ["images/a.jpg", "images/b.jpg"])
        self.assertTrue(groups[0]["caption"].startswith("Fig. 1."))
        self.assertIn("Yield stress", groups[0]["caption"])

    def test_fig_caption_immediately_after_image(self) -> None:
        md = """# T

# A

Abstract.

![](images/x.jpg)
Fig. 2. Single plot caption.

Next para.
"""
        groups = parse_markdown_text(md)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["image_paths"], ["images/x.jpg"])
        self.assertIn("Fig. 2.", groups[0]["caption"])

    def test_heading_style_figure_caption(self) -> None:
        md = """# Title

# Abstract

Abs.

![](images/p.jpg)

# Figure 1. Results overview

Following text.
"""
        groups = parse_markdown_text(md)
        self.assertEqual(len(groups), 1)
        self.assertTrue(groups[0]["caption"].startswith("Figure 1."))

    def test_parse_a22_cleaned_fixture_if_present(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        md_path = (
            repo.parent
            / "datasets"
            / "Al_82"
            / "Al_82_papers"
            / "output"
            / "A22"
            / "preprocess"
            / "cleaned_input.md"
        )
        if not md_path.exists():
            self.skipTest(f"missing fixture: {md_path}")
        groups = parse_markdown_text(md_path.read_text(encoding="utf-8"))
        with_caption = [g for g in groups if (g.get("caption") or "").strip()]
        self.assertGreaterEqual(len(with_caption), 1)
        first = with_caption[0]
        self.assertGreaterEqual(len(first["image_paths"]), 1)
        cap = first["caption"]
        self.assertTrue("Fig" in cap or "Figure" in cap)


if __name__ == "__main__":
    unittest.main()
