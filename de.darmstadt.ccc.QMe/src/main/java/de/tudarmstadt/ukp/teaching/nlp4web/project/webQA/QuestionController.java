package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QuestionController {

	//this is currently set up for testing. edit strings to let the controller generate questions from http requests
	//remember to edit the test if you change something here. otherwise .jar won't build.
	
    private static final String template = "%s";
    private final AtomicLong counter = new AtomicLong();

    @RequestMapping("/questionPost")
    public Question questionpost(@RequestParam(value="question", defaultValue="") String question, @RequestParam(value="requester", defaultValue="") String requester) {
        return new Question(counter.incrementAndGet(), String.format(template, question), String.format(template, requester));
    }
    
    @RequestMapping("/questionGet")
    public Question questionGet(@RequestParam(value="question", defaultValue="") String question, @RequestParam(value="requester", defaultValue="") String requester) {
        return new Question(counter.get(), String.format(template, question), String.format(template, requester));
    }
}
