import unittest

from paper_extractor.preprocess.image_groups import parse_markdown_text
from paper_extractor.preprocess.markdown_cleaner import clean_markdown_with_content_list


class PreprocessRegressionTest(unittest.TestCase):
    def test_image_groups_handle_fig_caption_noise_and_wrapped_image_paths(self) -> None:
        markdown = """# Paper Title

This abstract is intentionally long enough to be selected as the paper abstract instead of metadata.

# Results

The result is shown in Fig. 2(a). A related map is shown in Fig. 3.

![](images/abc
def.jpg)
MANGANESE (Wt.%)
Fig. 2. Effect of manganese and aluminum on oxidation.

![](images/ghi.jpg)

<details>
<summary>natural_image</summary>
OCR visual description.
</details>

Fig. 3. Oxide map for the alloy system.
"""

        groups = parse_markdown_text(markdown)

        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["image_paths"], ["images/abcdef.jpg"])
        self.assertEqual(groups[0]["caption"], "Fig. 2. Effect of manganese and aluminum on oxidation.")
        self.assertEqual(groups[0]["paper_title"], "Paper Title")
        self.assertTrue(groups[0]["paper_abstract"].startswith("This abstract"))
        self.assertEqual(groups[0]["citation_sentences"], ["The result is shown in Fig. 2(a). A related map is shown in Fig. 3."])
        self.assertEqual(groups[1]["caption"], "Fig. 3. Oxide map for the alloy system.")

    def test_content_list_cleaner_preserves_title_and_extracts_numbered_references(self) -> None:
        markdown = """# Paper Title

Body text.

Paper Title

# REFERENCES

1. First reference.
2. Second reference.
"""
        items = [{"type": "header", "text": "Paper Title"}]

        cleaned, references, removed_categories, removed_blocks = clean_markdown_with_content_list(markdown, items)

        self.assertTrue(cleaned.startswith("# Paper Title"))
        self.assertNotIn("\nPaper Title\n", cleaned)
        self.assertEqual(removed_categories, {"header": 1})
        self.assertEqual(removed_blocks, 1)
        self.assertEqual([ref["text"] for ref in references], ["1. First reference.", "2. Second reference."])


if __name__ == "__main__":
    unittest.main()
