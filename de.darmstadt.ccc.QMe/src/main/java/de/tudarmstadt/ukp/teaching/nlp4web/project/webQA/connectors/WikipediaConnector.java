package de.tudarmstadt.ukp.teaching.nlp4web.project.webQA.connectors;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.*;
import java.net.URL;
import java.nio.charset.Charset;
import java.util.HashSet;
import java.util.Set;

public class WikipediaConnector {

	private static final String URL_SEARCH = ".wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srsearch=";
    private static final String URL_PARSE = ".wikipedia.org/w/api.php?action=parse&format=json&prop=text&utf8=1&disablelimitreport=1&disableeditsection=1&disabletoc=1&page=";

    public static final int MAX_RESULTS = 10;

    public static String lang;
    
    
    /**
     * Get a list of relevant wikipedia articles
     *
     * @param searchTerm term to search for
     * @return a (potentially empty) list of relevant articles
     */
    public static Set<String> getWikipediaArticleIds(String searchTerm)
    {
        return getWikipediaArticleIds(searchTerm, MAX_RESULTS);
    }

    /**
     * Get a list of relevant wikipedia articles
     *
     * @param searchTerm term to search for
     * @return a (potentially empty) list of relevant articles
     */
    public static Set<String> getWikipediaArticleIds(String searchTerm, int maxResults)
    {
        Set<String> results = new HashSet<>();

        try {
            JSONObject jsonAnswer = _callAPI("https://"+lang+URL_SEARCH+searchTerm);

            // Get relevant information from json answer
            JSONObject joQuery = jsonAnswer.getJSONObject("query");
            JSONArray jaResults = joQuery.getJSONArray("search");

            // Loop over the first results...
            for(int i = 0; i < jaResults.length() && i < maxResults;i++)
            {
                // ...and store the article names
                JSONObject result = jaResults.getJSONObject(i);
                results.add(result.getString("title"));
            }
        }
        catch (IOException | JSONException e) {
            e.printStackTrace();
        }
        return results;
    }

    /**
     * Get the text of a given article
     *
     * @param pageName name of the article
     * @return text (may still contain html)
     */
    public static String getArticleText(String pageName)
    {
        pageName = pageName.replace(' ', '+');

        StringBuilder sb = new StringBuilder();
        try {
            JSONObject jsonAnswer = _callAPI("https://"+lang+URL_PARSE+pageName);
            
            // Get relevant information from json answer
            JSONObject joParse = jsonAnswer.getJSONObject("parse");
            JSONObject joText = joParse.getJSONObject("text");
            String text = joText.getString("*");

            // Store the text of all paragraphs in the result buffer
            Document doc = Jsoup.parse(text);
            Elements domElements = doc.select("p");
            for(Element element : domElements)
                sb.append(element.text().toLowerCase()).append(" ");
        }
        catch (IOException | JSONException e) {
            e.printStackTrace();
        }

        return sb.toString();
    }

    /**
     * Perform the raw url call and return a json object
     *
     * @param url url to call
     * @return json object
     * @throws IOException
     */
    private static JSONObject _callAPI(String url) throws IOException {
        InputStream is = new URL(url).openStream();
        BufferedReader rd = new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
        String jsonText = _readAll(rd);
        return new JSONObject(jsonText);
    }

    /**
     * Helper: Read the whole content of a stream into a single string
     *
     * @param rd reader to read
     * @return string containing content of the reader
     * @throws IOException
     */
    private static String _readAll(Reader rd) throws IOException {
        StringBuilder sb = new StringBuilder();
        int cp;
        while ((cp = rd.read()) != -1) {
            sb.append((char) cp);
        }
        return sb.toString();
    }
}
