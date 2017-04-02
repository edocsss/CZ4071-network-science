## Ssh to Graph02 (master node)
  ssh to grpNT06s@distgraph.scse.ntu.edu.sg, password is (see in WA)  
  `ssh grpNT06s@distgraph.scse.ntu.edu.sg`  
  
  ssh to graph02  
  `ssh graph02`  
  
## Setting up Environment Variables
Settings must be set up for running code in single node or distributed modes. We need to check if our code works in both modes.  


So, there are two folders under graph02: single_node and distributed. Each directory have its own setup.sh, so source the appropriate setup.sh according to which mode we want to use.  
`cd [single_node or distributed dir]`
`source setup.sh`
  
`setup.sh` will set up the appropriate hadoop, java, and giraph environment variables according to the mode that is being used.   

## Running Hadoop 
Check the running Hadoop before running anything. Prior to the following services, ensure that the correct environment variables for the mode have been setup (try `echo $HADOOP_HOME` and `echo $GIRAPH_HOME`).

### Stopping Hadoop Service
`$HADOOP_HOME/sbin/stop-all.sh`  

### Starting Hadoop Service
`$HADOOP_HOME/sbin/start-all.sh`  

### Checking Running Services
`jps`
For distributed: `NameNode`, `SecondaryNameNode`, `Jps` and `ResourceManager` should be displayed.
For single_node: available services in distributed + `NodeManager`.

## Copying Custom Java Files
You need to copy your code into the giraph/custom-code directory under both single_node and distributed directory.   
copy .java files into `[single_node or distributed]/giraph/custom-code`
  
## Running custom code
### Confirm Environment Variables and the Running Hadoop
Be careful about which mode you are using because the environment variables ($HADOOP_HOME and $GIRAPH_HOME) affect how the jar is generated. Same applies to the running Hadoop (single vs distributed), ensure that the correct Hadoop mode is running.
    
### Generating Jar  
  cd to the [single_node or distributed]/giraph/custom-code , then run generate-jar.sh using the .java file that you want to run.  
  `cd [single_node or distributed]/giraph/custom-code`  
  `./generate-jar.sh [JAVA_FILENAME].java`  
  This will generate the java class, a jar file that contains the Java class and its dependencies `custom-code.jar` in the current `custom-code` directory, and copy the jar dependencies to the shared hadoop folder.  
    
### Running Code  
  Under the custom-code directory. Just edit, copy and run the following code. Note that the JAVA_FILENAME, is the generated java class name without the .class extension. So if you have `PageRankComputation.class`, just use `PageRankComputation` only.
  
#### Distributed
  `$HADOOP_HOME/bin/hadoop jar custom-code.jar org.apache.giraph.GiraphRunner [JAVA_FILENAME] --yarnjars custom-code.jar -w 1 -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat -vip /input/[txt_input] -vof org.apache.giraph.io.formats.IdWithValueTextOutputFormat  -op /output/[directory_output]`  
  
#### Single Node
 `$HADOOP_HOME/bin/hadoop jar custom-code.jar org.apache.giraph.GiraphRunner [JAVA_FILENAME] -w 1 -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat -vip /input/[txt_input] -vof org.apache.giraph.io.formats.IdWithValueTextOutputFormat -op /output/[directory_input] -ca giraph.SplitMasterWorker=false`

### Hadoop File System (output, input)
- For input and output, please read the relevant documentation about Hadoop File system  
[Link to HDFS 2.6.0](https://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-common/FileSystemShell.html)
- Listing existing file: -ls
  - input: `$HADOOP_HOME/bin/hadoop dfs -ls /input`  
  - output: `$HADOOP_HOME/bin/hadoop dfs -ls /output`  
- Reading: -cat
- Uploading file: -put
  `$HADOOP_HOME/bin/hadoop dfs -put [input_file] [hadoop input directory]`  
