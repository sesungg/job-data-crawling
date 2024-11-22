package com.job.job;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Job {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String companyName;
    private String title;
    private String url;
    private String career;
    private String education;
    private String employmentType;
    private String location;
    private String deadline;

    private Job(String companyName, String title, String url, String career, String education, String employmentType, String location, String deadline) {
        this.companyName = companyName;
        this.title = title;
        this.url = url;
        this.career = career;
        this.education = education;
        this.employmentType = employmentType;
        this.location = location;
        this.deadline = deadline;
    }

    public static Job of(String companyName, String title, String url, String career, String education, String employmentType, String location, String deadline) {
        return new Job(
                companyName,
                title,
                url,
                career,
                education,
                employmentType,
                location,
                deadline
        );
    }
}
