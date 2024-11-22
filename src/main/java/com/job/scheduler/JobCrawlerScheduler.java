package com.job.scheduler;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.job.job.Job;
import com.job.job.JobRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.batch.BatchProperties;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class JobCrawlerScheduler {

    private final JobRepository jobRepository;

    @Scheduled(cron = "0 0 * * * *")
    public void executePythonScript() {
        try {
            // 파이썬 스크립트 경로
            String scriptPath = "/python-crawling/scrape_jobkorea.py";

            // ProcessBuilder 를 사용하여 파이썬 실행
            ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath);
            Process process = processBuilder.start();

            // 스크립트 출력 읽기
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder jsonOutput = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                jsonOutput.append(line);
            }

            ObjectMapper objectMapper = new ObjectMapper();
            List<Map<String, Object>> jobDataList = objectMapper.readValue(jsonOutput.toString(), List.class);

            for (Map<String, Object> jobData : jobDataList) {
                Job job = Job.of(
                        (String) jobData.get("company_name"),
                        (String) jobData.get("title"),
                        (String) jobData.get("url"),
                        (String) jobData.get("career"),
                        (String) jobData.get("education"),
                        (String) jobData.get("employment_type"),
                        (String) jobData.get("location"),
                        (String) jobData.get("deadline")
                );

                jobRepository.save(job);
            }

            System.out.println("크롤링 데이터를 데이터베이스에 저장했습니다.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
