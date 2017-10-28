package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Random;

import org.apache.uima.UIMAException;

import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.pipeline.WebPipeline;

public class Question {

    private final long id;
    private final String content;
    private String answer;
    private final String requester;

    public Question(long id, String content, String requester) {
        this.id = id;
        this.content = content;
        this.answer = "test answer";
        this.requester = requester;
    }

    public long getId() {
        return id;
    }
    
    public void setAnswer(String answer) {
    	this.answer = answer;
    }
    
    public String getRequester(){
    	return "@" + this.requester;
    }
    
    public String getAnswer() throws UIMAException, IOException {
    	
    	if(!content.equals("")){
    		//we store questions and answers at these paths because the UIMA Pipeline works with local files
        	String questionPath = "./Question" + Long.toString(this.id) +".txt";
        	//create Question File
        	try(  PrintWriter out = new PrintWriter( questionPath )  ){
        	    out.println( content );
        	}
        	setAnswer("");
        	
    	}
    	else{
    		Random randomGenerator = new Random();
        	long qn = nextLong(randomGenerator, this.id);
        	String answerPath = "./Question" + Long.toString(qn) + ".txt";
        	setAnswer(readFile(answerPath));
    	}
    	
        return this.answer;
    }

    public String getContent(){
        return this.content;
    }
    
    private String readFile(String file) throws IOException {
    	File f = new File(file);
	    	if(f.exists() && !f.isDirectory()) { 
		    	    // do something
		    	
		        BufferedReader reader = new BufferedReader(new FileReader (file));
		        String         line = null;
		        StringBuilder  stringBuilder = new StringBuilder();
		        String         ls = System.getProperty("line.separator");
		
		        try {
		            while((line = reader.readLine()) != null) {
		                stringBuilder.append(line);
		                stringBuilder.append(ls);
		            }
		
		            return stringBuilder.toString();
		        } finally {
		            reader.close();
		        }
	    	}
	    	else{
	    		return "";
	    	}
    }
    
    private long nextLong(Random rng, long n) {
    	   // error checking and 2^x checking removed for simplicity.
    	   long bits, val;
    	   do {
    	      bits = (rng.nextLong() << 1) >>> 1;
    	      val = bits % n;
    	   } while (bits-val+(n-1) < 0L);
    	   
    	   return val+1;
    	}

}
