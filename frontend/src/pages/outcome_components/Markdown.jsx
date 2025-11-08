import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { defaultSchema } from "hast-util-sanitize";

const katexSchema = {
  ...defaultSchema,
  tagNames: [
    ...(defaultSchema.tagNames || []),
    // Common KaTeX/MathML tags:
    "span",
    "math",
    "semantics",
    "mrow",
    "mi",
    "mn",
    "mo",
    "msup",
    "msub",
    "mfrac",
    "mover",
    "munder",
    "munderover",
    "mtable",
    "mtr",
    "mtd",
    "annotation",
  ],
  attributes: {
    ...defaultSchema.attributes,
    span: [
      ...(defaultSchema.attributes?.span || []),
      ["className"], // needed for KaTeX styling
      ["style"], // optional; only if you need inline styles
    ],
    math: [["xmlns"]],
    annotation: [["encoding"]],
  },
};

const Markdown = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[
        [rehypeRaw],
        [rehypeKatex],
        [rehypeSanitize, katexSchema],
      ]}
    >
      {content}
    </ReactMarkdown>
  );
};

export default Markdown;
