package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.writer;


import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.connectors.WikipediaConnector;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.*;

import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasConsumer_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.text.BreakIterator;
import java.util.*;
import java.util.stream.Collectors;


public class QuizResultWriter extends JCasConsumer_ImplBase {

	public static final String TESTMODE = "TEST_MODE";
	@ConfigurationParameter(name = TESTMODE,
			description = "Test Mode (correct answer given)",
			mandatory = true)
	private Boolean testMode;
	
	public static final String LANG = "LANG";
	@ConfigurationParameter(name = LANG,
			description = "Language",
			mandatory = true)
	private String lang;
	
	public static final String FILE = "FILE";
	@ConfigurationParameter(name = FILE,
			description = "Name of the File where the answer will be stored",
			mandatory = true)
	private String answerPath;

	private static final String LF = System.getProperty("line.separator");

	private Set<String> articleList;
	private LinkedList<String> articleTexts;

	public void process(JCas jcas) throws AnalysisEngineProcessException {
		StringBuilder sb = new StringBuilder();
		
		WikipediaConnector.lang = lang;

        for (Annotation question : JCasUtil.select(jcas, Question.class)) {
        	articleList = new HashSet<>();
			articleTexts = new LinkedList<>();
			String bestAnswer = "";
            int bestScore = 0;
            boolean answerFound = false;

			sb.append("Question: ").append(question.getCoveredText()).append(LF);

			// Take keywords:
			Collection<Keyword> keywords = JCasUtil.select(jcas, Keyword.class);

			// Try to find directly matching wikipedia articles
			findExactArticleMatches(keywords);

			// Not successful?
			if(articleList.size() == 0)
			{
				// Try finding partial results
				findPartialArticleMatches(keywords);

				// No answer possible if there are still no results
				if(articleList.size() == 0)
				{
					sb.append("Not able to answer").append(LF);
					break;
				}
			}

			// Load article contents
			articleTexts.addAll(articleList.stream().map(WikipediaConnector::getArticleText).collect(Collectors.toList()));

			// Compare with answers
			for(Annotation answer : JCasUtil.select(jcas, Answer.class)) {
				String answerText = answer.getCoveredText();
				List<AnswerKeyword> answerKeywords = JCasUtil.selectCovered(jcas, AnswerKeyword.class, answer.getBegin(), answer.getEnd());

				int score = computeScore(answerKeywords);
				if(score > bestScore)
				{
					bestAnswer = answerText;
					bestScore = score;
					answerFound = true;
				}
			}

            // Display answer
			if(answerFound)
				sb.append("Answer: ").append(bestAnswer).append(" (").append(bestScore).append(")").append(LF);
			else
				sb.append("No answer found").append(LF);


            // Test mode? Assess correctness
			if(answerFound && testMode)
			{
				for (Annotation correctAnswer : JCasUtil.select(jcas, CorrectAnswer.class)) {
					String correct_answer_text = correctAnswer.getCoveredText();
					if(bestAnswer.equals(correct_answer_text))
						sb.append("Correct").append(LF);
					else
						sb.append("Wrong (Answer was: ").append(correct_answer_text).append(")").append(LF);
				}
			}
        }

		System.out.print(sb.toString());
		
		//write answer to file
		try(  PrintWriter out = new PrintWriter(answerPath) ){
    	    out.println( sb.toString() );
    	} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Find wikipedia articles matching all keywords
	 * @param keywords collection of keywords
     */
	private void findExactArticleMatches(Collection<Keyword> keywords)
	{
		// Concatenate all
		StringBuilder sb = new StringBuilder();
		for(Keyword keyword : keywords)
		{
			sb.append(keyword.getCoveredText()).append("+");
		}

		// Load wikipedia articles
		articleList.addAll(WikipediaConnector.getWikipediaArticleIds(sb.toString()));
	}

	/**
	 * Find wikipedia articles matching at least one keyword
	 * @param keywords collection of keywords
	 */
	private void findPartialArticleMatches(Collection<Keyword> keywords)
	{
		int articlesPerKeyword = Math.max(2, (int)Math.ceil(WikipediaConnector.MAX_RESULTS / keywords.size()));

		// Loop over all keywords and search individually
		for(Keyword keyword : keywords)
		{
			Set<String> tmpArticleList = WikipediaConnector.getWikipediaArticleIds(keyword.getCoveredText(), articlesPerKeyword);
			articleList.addAll(tmpArticleList);
		}
	}

	/**
	 * Compute score for a given answer
	 * @param answerWords answer words to score
	 * 	@return resulting score (absolute)
     */
	private int computeScore(List<AnswerKeyword> answerWords)
	{
		int score = 0;

		// For every word in the answer (usually one)...
		for(AnswerKeyword answerWord : answerWords)
		{
			String answerWordText = answerWord.getCoveredText();
			// ...and every related text...
			for(String text : articleTexts)
			{
				BreakIterator bi = BreakIterator.getWordInstance();
				bi.setText(text);

				int start = bi.first();
				for (int end = bi.next();end != BreakIterator.DONE;start = end, end = bi.next()) {
					String word = text.substring(start, end);

					// ...count the absolute occurrences...
					if (word.equals(answerWordText))
						score++;
				}
			}
		}

		// ...and return that score
		return score;
	}
}
