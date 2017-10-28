package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.reader;

import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.Answer;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.CorrectAnswer;
import de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.type.Question;
import org.apache.uima.UimaContext;
import org.apache.uima.collection.CollectionException;
import org.apache.uima.fit.component.JCasCollectionReader_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.util.Progress;
import org.apache.uima.util.ProgressImpl;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

public class QuizReader extends JCasCollectionReader_ImplBase {

    public static final String FILE = "FILE";
	@ConfigurationParameter(name = FILE,
			description = "file path",
			mandatory = true)
	private String filePath;

	public static final String TESTMODE = "TEST_MODE";
	@ConfigurationParameter(name = TESTMODE,
			description = "Test Mode (correct answer given)",
			mandatory = true)
	private Boolean testMode;

	private int idx = 0;
    private Scanner scanner;

	@Override
	public void initialize(UimaContext context) throws ResourceInitializationException {
		super.initialize(context);
		
        try {
            File f = new File(filePath);
            scanner = new Scanner(f);
        } catch (NullPointerException | FileNotFoundException e) {
            e.printStackTrace();
        }
    }

	@Override
	public void getNext(JCas jcas) throws IOException, CollectionException {
        // Read line by line
        String line = scanner.nextLine().toLowerCase();

        // Set line as text of jcas
		jcas.setDocumentText(line);

		int start = 0;
		int end = -1;
		boolean isQuestion = true;

		// Loop over all characters in line
		while(end < line.length() -1)
		{
			// Found a semicolon?
			if(line.substring(end+1, end+2).equals(";"))
			{
				// If it is the first one, the text unit now contains the question
				if(isQuestion)
				{
					Question annotation = new Question(jcas, start, end+1);
					annotation.addToIndexes();
					isQuestion = false;
				}
				// Otherwise, it was an answer
				else
				{
					Answer annotation = new Answer(jcas, start, end+1);
					annotation.addToIndexes();
				}
				start = end + 2;
			}
			end++;
		}

		// Add the last answer (no trailing semicolon)
		if(start < end)
		{
			// In test mode, the last answer is the correct answer (repeated)...
			if(testMode)
			{
				CorrectAnswer annotation = new CorrectAnswer(jcas, start, end+1);
				annotation.addToIndexes();
			}
			// ...otherwise it is a normal answer
			else
			{
				Answer annotation = new Answer(jcas, start, end+1);
				annotation.addToIndexes();
			}
		}

		idx++;
	}

	@Override
	public Progress[] getProgress() {
		int size = Integer.MAX_VALUE;
		return new Progress[] { new ProgressImpl(idx + 1, size, Progress.ENTITIES) };
	}

	@Override
	public boolean hasNext() throws IOException, CollectionException {
        if( scanner.hasNext())
            return true;

        scanner.close();
		return false;
	}
}
