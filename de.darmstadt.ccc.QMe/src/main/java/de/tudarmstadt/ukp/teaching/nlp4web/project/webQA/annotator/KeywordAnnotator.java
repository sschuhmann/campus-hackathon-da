package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.annotator;

import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.Answer;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.AnswerKeyword;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.Keyword;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.Question;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasAnnotator_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;

import java.text.BreakIterator;
import java.util.Iterator;
import java.util.Set;

public class KeywordAnnotator extends JCasAnnotator_ImplBase
{
    public static final String STOPWORDS = "STOPWORDS";
    @ConfigurationParameter(name = STOPWORDS,
            description = "Set of Stopwords",
            mandatory = true)
    private Set<String> stopwords;



    // Find keywords (not stopwords_de)
    @Override
    public void process(JCas jcas)
        throws AnalysisEngineProcessException
    {
        // Analyze words from question only
        Iterator<Question> iterator = JCasUtil.select(jcas, Question.class).iterator();
        if(!iterator.hasNext())
            return;

        Annotation question = iterator.next();
        String document = question.getCoveredText();

		BreakIterator bi = BreakIterator.getWordInstance();
		bi.setText(document);
		
		int start = bi.first();
		for (int end = bi.next();end != BreakIterator.DONE;start = end, end = bi.next()) 
		{
			String word = document.substring(start,end);

            // No stopword? Then it is a keyword
            if(!is_stopword_or_blank(word, stopwords))
            {
                Keyword tokenAnnotation = new Keyword(jcas);
                tokenAnnotation.setBegin(start);
                tokenAnnotation.setEnd(end);
                tokenAnnotation.addToIndexes();
            }
		}

		/*
		    Analyze Answers
		 */
        for(Annotation answer : JCasUtil.select(jcas, Answer.class)) {
            String answerText = answer.getCoveredText();

            bi.setText(answerText);

            start = bi.first();
            for (int end = bi.next();end != BreakIterator.DONE;start = end, end = bi.next())
            {
                String word = answerText.substring(start,end);

                // No stopword? Then it is a keyword
                if(!is_stopword_or_blank(word, stopwords))
                {
                    AnswerKeyword tokenAnnotation = new AnswerKeyword(jcas);
                    tokenAnnotation.setBegin(start + answer.getBegin());
                    tokenAnnotation.setEnd(end + answer.getBegin());
                    tokenAnnotation.addToIndexes();
                }
            }
        }
    }

    /**
     * Check whether the given word is a stopword (or no word at all)
     *
     * @param word word to check
     * @param stopwords list of stopwords
     * @return true if stopword or punctuation
     */
    private static boolean is_stopword_or_blank(String word, Set<String> stopwords) {
        // Check for whitespace & punctuation
        // Check for stopword
        return !(!word.equals(" ") && Character.isLetterOrDigit(word.charAt(0))) || stopwords.contains(word);
    }
}