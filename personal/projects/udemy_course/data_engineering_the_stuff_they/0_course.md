# Data Engineering: The Stuff They Didn't Teach You

## Course Description
If you've been learning data engineering, you might feel comfortable reading files, transforming them into parquet or delta format, and loading them into various cloud data platforms. You've got the basics nailed down.

But then, in your new job, you hear terms like *surrogate key*, *SCD2*, and *metadata columns--and suddenly, you realize there's a whole other side to data engineering that tutorials never taught you. When you ask your favorite AI tools, the answers can feel disconnected from the real-world context you actually need.

That's where **Data Engineering: The Stuff They Didn't Teach You** comes in. This course assumes you already know the fundamentals of Data Engineering (like reading data from files and doing transformations). From there, we'll dive into practical, real-world concepts, so you can deal with everyday challenges like a pro. This course distills the solutions to common pitfalls that data engineers encounter, explaining what these pitfalls are and how to approach them effectively.

This course will be SQL-focused. You will find that the longer you are in the Data Engineering space, the more you might use SQL over Python. Luckily, this should only affect the implementation sections of the course, but the concepts are still incredibly important.

(I used to strictly develop my pipelines in Python, but grew to understand why SQL is the lingua franca.)

I am considering a Python-focused edition though!

## Course Outline

### 1. Introduction to Real-World Data Engineering
- Beyond the basics: why conceptual knowledge matters
- Challenges that tutorials gloss over
- Some DevOps concepts: Dev, Test, Prod
- Understanding OLTP vs. OLAP

### 2. Data Modeling Fundamentals
- Star schema vs. Snowflake schema
- Common data modeling techniques
- Fact tables and dimension tables

### 3. Metadata Columns
- What they are and why they matter
- Common metadata columns (timestamps, lineage, operational flags)
- Creating custom metadata columns for tracking

### 4. Surrogate Keys
- Definition and role in dimension tables
- How to select candidate columns for surrogate keys
- Hashing strategies (SHA, MD5, and more)
- Best practices for surrogate key generation

### 5. Slowly Changing Dimensions (SCD)
- Why dimensions need change tracking
- Types of SCD (Type 1, Type 2, etc.)
- Practical implementations with examples

### 6. Incremental Load vs. Full Load
- When to choose incremental vs. full loads
- Using existing metadata columns for incremental loads
- Hash-based incremental loads
- When and how to do full loads

### 7. Snapshots
- The importance of snapshot data for historical context
- Techniques for snapshotting fact tables
- Managing snapshot frequency and size

### 8. Masking Private Information
- Why data masking is crucial for compliance and security
- Common masking techniques and tools
- Balancing data utility with privacy requirements

### 9. Additional Topics & Real-World Considerations
- Schema evolution and handling breaking changes
- Performance tuning and indexing strategies
- Working with data quality checks and observability tools
