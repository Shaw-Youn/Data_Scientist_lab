#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


# In[2]:


# Create a Spark session with Delta Lake configurations
spark = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()





# In[3]:


spark.sparkContext.setLocalProperty('spark.scheduler.pool','pool_1')


# In[4]:


df = spark.read.csv('/Users/xwyang/Desktop/data/flights.csv',header=True,inferSchema=True)


# In[5]:


df.show(10)


# In[6]:


df.columns


# In[7]:


spark.sql('show tables').show()


# In[9]:


df.write.format('parquet').mode('overwrite').saveAsTable('pooltbl_1')


# In[10]:


spark.table('pooltbl_1').show(10)


# In[11]:


spark.sql("""  create table if not exists pool_scheduler_tbl 
using csv options(path'/Users/xwyang/Desktop/data/flights.csv',header=True,inferSchema=True)    
""")


# In[12]:


spark.read.table('pool_scheduler_tbl').show(5)


# In[13]:


spark.sql("""select date,delay,distance,origin,destination,
case when delay < 0 then'Early' 
     when delay between 20 and 100 then'on-time'
     when delay >100 and delay <200 then 'minor-delay'
     Else 'delay' end as status
     from pool_scheduler_tbl
""").show(10)


# In[14]:


spark.sql('show tables').show()


# In[15]:


deltaPath='/Users/xwyang/Desktop/delta_dir'


# In[16]:


dff = spark.table('pooltbl_1')


# In[17]:


dff.show(10)


# In[19]:


dff.write.format('delta').mode('overwrite').save(deltaPath)


# In[20]:


spark.conf.set("spark.sql.debug.maxToStringFields", "1000")


# In[21]:


delta_df = spark.read.format('delta').load(deltaPath)


# In[22]:


delta_df.show(10)


# In[23]:


delta_df.printSchema()


# In[24]:


delta_df.explain()


# In[25]:


spark.read.format('delta').load(deltaPath).createOrReplaceTempView('delta_tbl')


# In[26]:


spark.sql('show tables').show()


# In[27]:


spark.sql(""" select * from delta_tbl limit 5  """).show()


# In[28]:


spark.sql("""  select count(*) as total_counts from delta_tbl""").show()


# In[30]:


spark.sql("""  select origin, count(*) as total_counts 
from delta_tbl group by origin order by total_counts DESC limit 10""").show()


# **Loading Data Streams into a Delta Lake Table**
# As with static DataFrames, you can easily modify your eisting Structured Streaming jobs to write to and read from a Delta Lake table by setting the format to 'delta'. Say you have a stream of data as a DataFrame named NewStreamDF,which has the same schema as the table. You can append to the table as follows:
# 
# ```
# 
#  delta_query = (NewStreamDF.writeStream
#                            .format('delta')
#                            .outputMode('append')
#                            .option('checkpointLocation',check_dir)
#                            .trigger(processingTime='10 seconds')
#                            .start(deltaPath))
#  ```

# In[ ]:




