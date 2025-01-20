# Data Engineering: The Stuff They Didnt Teach You 

## Introduction 

At this point, you've watched many tutorials about how to be a data engineer

If its on the cloud, they probably taught you how to read a file, turn it into a parquet or a delta table or whatever

Do some transformations on it 

Then save it into the databases that you have in the cloud. Maybe Snowflake, maybe Databricks, maybe Fabric

You got the job, you're confident

Then your coworker says the words "surrogate key", "SCD2", "metadata columns"

And in your head you go "...What?"

`Data Engineering: The Stuff They Didnt Teach You` is for you

This course assumes some basic understanding of Data Engineering (literally every course on udemy), and then extends them with *real-world* concepts that you *should* know to do your job right. You will find that when you are implementing data engineering concepts, you will encounter challenges--luckily, a lot of people have encountered these problems before, here are some common pitfalls, what they mean and how to approach them

## Course Outline

- metadata columns
  - common metadata columns and what they're for
  - implementing your own
- what is a surrogate key? 
  - hashing
    - types of hashing
    - which hashing technique to use and why
  - how to select candidate columns
- facts
- dims
- slowly changing dimensions
  - how to implement them
- incremental load vs full load
  - how to do an incremental load
    - doing an incremental load using existing metadata columns in the source
    - doing an incremental load using hashes
  - how to do a full load
- masking "private" information
- snapshots
