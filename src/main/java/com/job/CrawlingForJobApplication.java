package com.job;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class CrawlingForJobApplication {

    public static void main(String[] args) {
        SpringApplication.run(CrawlingForJobApplication.class, args);
    }

}
