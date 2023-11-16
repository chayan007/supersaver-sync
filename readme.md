# Training Model

This is a classification problem where we classify bank narrations into different categories using our Deep Learning-based model. To enhance accuracy, we've implemented several unique strategies:
- **Sub-word Level Tokenization:** We utilize sub-word level tokenization to handle misspellings or truncated words, ensuring accurate categorization (e.g., "baj fin" categorized as "Loan" from "bajaj finance - Loan").
- **Training Word Embeddings from Scratch:** Custom-trained embeddings tailored for finance data.
- **Custom Loss Function:** Implemented for enhanced training accuracy.
- **Quantization:** Reduced model size from **500MB** to **150MB** with minimal accuracy loss **(<0.1%)**.
- **Separate Models for Credit and Debit Transactions:** Different models for each transaction type.

## Salary Extraction

Our model identifies salary transactions by detecting keywords in bank narrations or using a clustering-based algorithm for periodic credits. It handles various edge cases:
- Changes in companies.
- Simultaneous salary credits from multiple organizations.
- Salary credits from loan providers. 
Our accuracy in identifying salary transactions stands at **91%**.

## Model Inference Process and Accuracy

We use multithreading to load and predict on the model, achieving rapid processing (less than 1 sec for 1000 records). Regex-based rule engines complement the model's classifications.
The entire system processes predictions within **3 seconds** on an 8-core machine, outperforming existing vendors. Real-world data shows a model accuracy of around **93%**, reaching **98%** with soft rules.

# UPI Categorization

Around 95% of user transactions are UPI-based, often lacking merchant or individual names in the narration, making classification challenging.
Proposed solution:
- Extract UPI IDs from the narration.
- Partner with a 3rd party for Merchant Name and Merchant Category Code.
- This collaboration enhances expenditure categorization, understanding user spending patterns, and facilitates comprehensive spending analysis for better recommendations.

