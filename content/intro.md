---
title: Pixels and Their Neighbours
short_title: Finite Volume
description: A tutorial of the finite volume method for the Direct Current (DC) resistivity problem.
license:
  content: CC-BY-4.0
keywords:
    - quantitative MRI
    - reproducibility
    - vendor-neutral
exports:
  - format: pdf
---

+++ { "part": "abstract" }

Magnetic resonance imaging has progressed significantly with the introduction of advanced computational methods and novel imaging techniques, but their wider adoption hinges on their reproducibility. This concise review synthesizes reproducible research insights from recent MRI articles to examine the current state of reproducibility in neuroimaging, highlighting key trends and challenges. It also provides a custom GPT model, designed specifically for aiding in an automated analysis and synthesis of information pertaining to the reproducibility insights associated with the articles at the core of this review.

+++

# Introduction

Reproducibility is a cornerstone of scientific inquiry, particularly relevant for data-intensive and computationally demanding fields of research, such as magnetic resonance imaging (MRI) {cite:p}`Stikov2019-hp`. Ensuring reproducibility thus poses a unique set of challenges and necessitates the diligent application of methods that foster transparency, verification, and interoperability of research findings. 

While numerous articles have addressed the reproducibility of clinical MRI studies, few have looked at the reproducibility of the MRI methodology underpinning these studies. This is understandable given that the MRI development community is smaller, driven by engineers and physicists, with modest representation from clinicians and statisticians. 

However, performing a thorough meta-analysis or a systematic review of these studies in the context of reproducibility presents challenges due to: 

* i) the diversity in study designs across various MRI development subfields, and 
* ii) the absence of standardized statistics to gauge reproducibility performance. 

:::{tip} Purpose
Considering these challenges, we opted to conduct a mini-review leveraging the semantic extraction capabilities of the advanced language models. Specifically, we trained a custom **GPT** model using a knowledge base constructed for a selection of articles coupled with web scraping of content pertaining to their reproducibility.
:::

With this mini-review we aim to examine the current landscape of reproducible research practices across various MRI studies, drawing attention to common strategies, tools, and repositories used to achieve reproducible outcomes. We anticipate that this approach provides a living review that can be automatically updated to accommodate the continuously expanding breadth of methodologies, helping us identify commonalities and discrepancies across studies.

# Methodology 

In distilling reproducibility insights powered by GPT, this review centered on 31 research articles published in the journal Magnetic Resonance in Medicine (MRM), chosen by the editor for their dedication to enhancing reproducibility in MRI. Since 2020, the journal has published interviews with authors of these selected publications, discussing the tools and practices they used to bolster the reproducibility of their findings (available [here](https://blog.ismrm.org/category/highlights)).

## Mapping selected articles in the semantic landscape of reproducibility

We performed a literature search to identify where these studies fall in the broader literature of reproducible neuroimaging. To retrieve articles dedicated to reproducibility in MRI, we utilized the Semantics Scholar API [2] with the following query terms on November 23, 2023: 

```{code}
(code | data | open-source | github | jupyter ) & ((MRI & brain) | (MRI neuroimaging)) & reproducib~.
```

Among `1098` articles included in the Semantic Scholar records, SPECTER vector embeddings {cite:p}`Cohan2020-tw` were available for `612` articles, representing the semantics of publicly accessible content in abstracts and titles. For these articles, the high-dimensional semantic information captured by the word embeddings was visualized using UMAP {cite:p}`McInnes2018-sc` [](#fig1stat). This visualization allowed the inspection of the semantic clustering of the articles, facilitating a deeper understanding of their contextual placement within the reproducibility landscape. In addition, the following diagram illustrates the hierarchical clustering of the selected studies in the broader literature:

```{mermaid}
:align: center
flowchart LR
  subgraph Data collection
  A[/Query terms/] --> B
  E[Web scrape] -- 31 --> F>MRM Highlight interviews]
  end
  B[[Semantic Scholar API]] -- 1098 --> C>Total records]
  C>Total records] --612--> D>Records w/ embedding]
  D --31--> H>MRM Articles]
  F -- match --> D
  D --> G(((UMAP)))
```

## Creating a knowledge base for a custom GPT

We created a custom GPT model, designed specifically to assist in the analysis and synthesis of information pertaining to the `31` reproducible research insights. The knowledge base of this retrieval-augmented generation framework incorporates GPT-4 summaries of the abstracts from `31` MRM articles, merged with their respective MRM Highlights interviews, as well as the titles and keywords associated with each article (refer to Appendix A). This compilation was assembled via API calls to OpenAI on November 23, 2023, using the `gpt-4-1106-preview` model.

```{mermaid}
:align: center
flowchart LR
  A>MRM Highlights Interviews] --> C
  B>Respective MRM Articles]--> C
  C(combine) --> D(((GPT-4)))
  D --> G[(Summary)]
  G --> H
  D --> H["Custom GPT"]
  subgraph RRInsights
  H <--> I[User]
  end
```

This specialized GPT, named `RRInsights`, is tailored to process and interpret the provided data in the context of reproducibility, for the system prompts please see Appendix B. 


# Results

## Contextual placement of the selected articles in the landscape of reproducibility

The MRI systems cluster was predominantly composed of articles published in MRM, with only two publications appearing in a different journal {cite:p}`Adebimpe2022-zp,Tilea2009-zu`. Additionally, this cluster was sufficiently distinct from the rest of the reproducibility literature, as can be seen by the location of the dark red dots [](#fig1). Few other selected articles (`8/31`) were found at the intersection of the MRI systems, deep learning, and data/workflows clusters, which in total spans `103` articles. Since the custom GPT model was trained on the `31` selected MRM articles (red dots), [](#fig1) serves as a map for inferring the topics where RRInsights is more likely to be context-aware.

::::{seealso} Click here to see the static version of the SAKURA plot
:class: dropdown
:::{figure} fig1static.jpg
:label: fig1stat
:width: 80%
:align: center
An embedded video with a caption!
:::
::::

:::{figure} #fig1-cell
:label: fig1
Edge-bundled connectivity of the 612 articles identified by the literature search. A notable cluster is formed by most of the MRM articles that were featured in the reproducible research insights (purple nodes), particularly in the development of MRI systems. Few other selected articles fell at the intersection of MRI systems, deep learning, and workflows. Notable clusters for other studies (pink) are annotated by gray circles.
:::


::::{seealso} Click here to see 3D UMAP scatter
:class: dropdown
:::{figure} #fig13d-cell
:label: fig2
Edge-bundled connectivity of the 612 articles identified by the literature search. A notable cluster is formed by most of the MRM articles that were featured in the reproducible research insights (purple nodes), particularly in the development of MRI systems. Few other selected articles fell at the intersection of MRI systems, deep learning, and workflows. Notable clusters for other studies (pink) are annotated by gray circles.
:::

::::

:::{figure} #anan-cell
:label: fig3
EH
:::


## Custom GPT for reproducibility insights

Through its advanced natural language processing capabilities, RRInsights can efficiently analyze the scoped literature, extract key insights, and generate comprehensive overviews of the research papers focusing on MRI technology. The custom GPT is available at https://chat.openai.com/g/g-5uDwBlnx4-rrinsights (requires subscription as of May 2024).



:::{figure} #gptsession

Automated interaction with GPT4, iterating over all (31) seleted records
:::


Figure 3 presents an example interaction with RRInsights to create a summary about the vendor-neutral solutions found in the knowledge base. The model's response to this inquiry demonstrates that RRInsights is context-aware, adept at pinpointing relevant information in the knowledge base, and offering interpretations within the framework of reproducibility. The following sub-sections are written based on the interactions with RRInsights:
