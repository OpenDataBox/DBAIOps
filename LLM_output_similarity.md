## LLM Output Similarity Assessment

We assess the similarity between **LLM outputs** and **input graph content** using **character-level** (i.e., Levenshtein distance) and **word-level** (i.e., TF-IDF) metrics.
For PostgreSQL anomalies, we obtain similarity scores of 0.10 and 0.37, showing that the outputs are not merely copied from the knowledge graph.

<table><thead>
  <tr>
    <th class="tg-7btt" rowspan="2">Method</th>
    <th class="tg-7btt" colspan="4">PostgreSQL</th>
    <th class="tg-7btt" colspan="4">Oracle</th>
  </tr>
  <tr>
    <th class="tg-7btt">difflib</th>
    <th class="tg-7btt">Levenshtein</th>
    <th class="tg-7btt">Jaccard</th>
    <th class="tg-7btt">TF-IDF</th>
    <th class="tg-7btt">difflib</th>
    <th class="tg-7btt">Levenshtein</th>
    <th class="tg-7btt">Jaccard</th>
    <th class="tg-7btt">TF-IDF</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-7btt">DBAIOps<br>(DeepSeek-R1 32B)</td>
    <td class="tg-c3ow">0.04</td>
    <td class="tg-c3ow">0.07</td>
    <td class="tg-c3ow">0.20</td>
    <td class="tg-c3ow">0.30</td>
    <td class="tg-c3ow">0.04</td>
    <td class="tg-c3ow">0.05</td>
    <td class="tg-c3ow">0.15</td>
    <td class="tg-c3ow">0.39</td>
  </tr>
  <tr>
    <td class="tg-7btt">DBAIOps<br>(DeepSeek-R1 671B)</td>
    <td class="tg-c3ow">0.04</td>
    <td class="tg-c3ow">0.10</td>
    <td class="tg-c3ow">0.24</td>
    <td class="tg-c3ow">0.37</td>
    <td class="tg-c3ow">0.05</td>
    <td class="tg-c3ow">0.09</td>
    <td class="tg-c3ow">0.29</td>
    <td class="tg-c3ow">0.50</td>
  </tr>
</tbody></table>