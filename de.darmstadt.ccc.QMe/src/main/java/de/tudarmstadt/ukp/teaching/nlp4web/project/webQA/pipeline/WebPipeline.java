package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.pipeline;

import static org.apache.uima.fit.factory.AnalysisEngineFactory.createEngine;
import static org.apache.uima.fit.factory.CollectionReaderFactory.createReader;

import java.io.IOException;
import java.util.Set;

import org.apache.uima.UIMAException;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.fit.pipeline.SimplePipeline;

import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.annotator.KeywordAnnotator;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.writer.QuizResultWriter;


import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.reader.QuizReader;
import de.tudarmstadt.ukp.teaching.nlp4web.project.Stopwords;;

public class WebPipeline{
	String lang = "de";
	public WebPipeline() {
		System.out.println("BOB");
	}
	
	public void RunPipeline(String questionPath, String answerPath) throws UIMAException, IOException {
		
		Set<String> stopwords = Stopwords.get(lang);
		
		CollectionReader reader = createReader(QuizReader.class,
				QuizReader.FILE, questionPath, 
				QuizReader.TESTMODE, false);

        AnalysisEngine ka = createEngine(KeywordAnnotator.class,
        		KeywordAnnotator.STOPWORDS, stopwords);
		
		AnalysisEngine writer = createEngine(QuizResultWriter.class, 
				QuizResultWriter.FILE, answerPath, 
				QuizResultWriter.LANG, lang,
				QuizResultWriter.TESTMODE, false);

		SimplePipeline.runPipeline(reader, ka, writer);
	}
}
