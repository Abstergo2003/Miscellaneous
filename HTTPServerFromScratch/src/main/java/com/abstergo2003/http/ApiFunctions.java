package com.abstergo2003.http;

import java.sql.Array;
import java.util.Arrays;
import org.json.JSONArray;

public class ApiFunctions {
    private HttpRequest request;

    public ApiFunctions(HttpRequest request) {
        this.request = request;
    }

    public static String parseFunction(HttpRequest request) {
        String target = request.getTarget();
        if (target.split("\\?")[0].contains("login")) {
            return Login(request);
        }
        return "undefined";
    }
    public static String Login(HttpRequest request) {
        JSONArray jsonArray = new JSONArray();
        jsonArray.put(request.getArgument("login"));
        jsonArray.put(request.getArgument("password"));
        return jsonArray.toString();
    }
}
