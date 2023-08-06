from proxycurl_py.config import (
    BASE_URL, PROXYCURL_API_KEY, TIMEOUT, MAX_RETRIES, MAX_BACKOFF_SECONDS
)
from proxycurl_py.gevent.base import ProxycurlBase
from proxycurl_py.models import (
    PersonEndpointResponse,
    PersonLookupUrlEnrichResult,
    ReverseEmailUrlEnrichResult,
    ExtractionEmailResult,
    PDLPhoneNumberResult,
    PDLEmailResult,
    ProfilePicture,
    PersonSearchResult,
    LinkedinCompany,
    CompanyUrlEnrichResult,
    JobListPage,
    JobListCount,
    EmployeeCount,
    EmployeeList,
    RoleSearchErichedResult,
    CompanyReveal,
    LinkedinSchool,
    StudentList,
    JobProfile,
    CreditBalance,
)


class _LinkedinPerson:
    def __init__(self, linkedin):
        self.linkedin = linkedin

    def get(
        self,
        extra: str,
        github_profile_id: str,
        facebook_profile_id: str,
        twitter_profile_id: str,
        personal_contact_number: str,
        personal_email: str,
        inferred_salary: str,
        skills: str,
        use_cache: str,
        fallback_to_cache: str,
        url: str,
    ) -> PersonEndpointResponse:
        """Person Profile Endpoint
        
                Cost: 1 credit / successful request.
        Get structured data of a Personal Profile
        
        :param extra: Enriches the Person Profile with extra details from external sources.
            Extra details include gender, birth date, industry and interests.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide extra data field.
            - `include` - Append extra data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type extra: str
        :param github_profile_id: Enriches the Person Profile with Github Id from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide Github Id data field.
            - `include` - Append Github Id data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type github_profile_id: str
        :param facebook_profile_id: Enriches the Person Profile with Facebook Id from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide Facebook Id data field.
            - `include` - Append Facebook Id data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type facebook_profile_id: str
        :param twitter_profile_id: Enriches the Person Profile with Twitter Id from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide Twitter Id data field.
            - `include` - Append Twitter Id data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type twitter_profile_id: str
        :param personal_contact_number: Enriches the Person Profile with personal numbers from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide personal numbers data field.
            - `include` - Append personal numbers data to the person profile object.
            Costs an extra `1` credit per email returned on top of the cost of the base endpoint (if data is available).
        :type personal_contact_number: str
        :param personal_email: Enriches the Person Profile with personal emails from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide personal emails data field.
            - `include` - Append personal emails data to the person profile object.
            Costs an extra `1` credit per email returned on top of the cost of the base endpoint (if data is available).
        :type personal_email: str
        :param inferred_salary: Include inferred salary range from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide inferred salary data field.
            - `include` - Append inferred salary range data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type inferred_salary: str
        :param skills: Include skills data from external sources.

            This parameter accepts the following values:
            - `exclude` (default value) - Does not provide skills data field.
            - `include` - Append skills data to the person profile object.
            Costs an extra `1` credit on top of the cost of the base endpoint (if data is available).
        :type skills: str
        :param use_cache: `if-present` The default behavior. Fetches profile from cache regardless of age of profile. If profile is not available in cache, API will attempt to source profile externally.

            `if-recent` API will make a best effort to return a fresh profile no older than 29 days.Costs an extra `1` credit on top of the cost of the base endpoint.
        :type use_cache: str
        :param fallback_to_cache: Tweaks the fallback behavior if an error arises from fetching a fresh profile.

            This parameter accepts the following values:
            * `on-error` (default value) - Fallback to reading the profile from cache if an error arises.
            * `never` - Do not ever read profile from cache.
        :type fallback_to_cache: str
        :param url: URL of the LinkedIn Profile to crawl.

            URL should be in the format of `https://www.linkedin.com/in/<public-identifier>`
        :type url: str
        :return: An object of :class:`proxycurl.models.PersonEndpointResponse` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.PersonEndpointResponse`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/v2/linkedin',
            params={
                'extra': extra,
                'github_profile_id': github_profile_id,
                'facebook_profile_id': facebook_profile_id,
                'twitter_profile_id': twitter_profile_id,
                'personal_contact_number': personal_contact_number,
                'personal_email': personal_email,
                'inferred_salary': inferred_salary,
                'skills': skills,
                'use_cache': use_cache,
                'fallback_to_cache': fallback_to_cache,
                'url': url,
            },
            data={
            },
            result_class=PersonEndpointResponse
        )

    def resolve(
        self,
        first_name: str,
        last_name: str,
        title: str,
        location: str,
        company_domain: str,
        enrich_profile: str,
    ) -> PersonLookupUrlEnrichResult:
        """Person Lookup Endpoint
        
                Cost: 2 credits / successful request.
        Look up a person with a name and company information.
        
        :param first_name: First name of the user
        :type first_name: str
        :param last_name: Last name of the user
        :type last_name: str
        :param title: Title that user is holding at his/her current job
        :type title: str
        :param location: The location of this user.

            Name of country, city or state.
        :type location: str
        :param company_domain: Company name or domain
        :type company_domain: str
        :param enrich_profile: Enrich the result with a cached profile of the lookup result.

            The valid values are:

            * `skip` (default): do not enrich the results with cached profile data
            * `enrich`: enriches the result with cached profile data

            Calling this API endpoint with this parameter would add 1 credit.

            If you require [fresh profile data](https://nubela.co/blog/how-fresh-are-profiles-returned-by-proxycurl-api/),
            please chain this API call with the [Person Profile Endpoint](https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint) with the `use_cache=if-recent` parameter.
        :type enrich_profile: str
        :return: An object of :class:`proxycurl.models.PersonLookupUrlEnrichResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.PersonLookupUrlEnrichResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/profile/resolve',
            params={
                'first_name': first_name,
                'last_name': last_name,
                'title': title,
                'location': location,
                'company_domain': company_domain,
                'enrich_profile': enrich_profile,
            },
            data={
            },
            result_class=PersonLookupUrlEnrichResult
        )

    def resolve_by_email(
        self,
        work_email: str,
        enrich_profile: str,
    ) -> ReverseEmailUrlEnrichResult:
        """Reverse Work Email Lookup Endpoint
        
                Cost: 3 credits / successful request.
        Resolve LinkedIn Profile from a work email address
        
        :param work_email: Work email address of the user
        :type work_email: str
        :param enrich_profile: Enrich the result with a cached profile of the lookup result.

            The valid values are:

            * `skip` (default): do not enrich the results with cached profile data
            * `enrich`: enriches the result with cached profile data

            Calling this API endpoint with this parameter would add 1 credit.

            If you require [fresh profile data](https://nubela.co/blog/how-fresh-are-profiles-returned-by-proxycurl-api/),
            please chain this API call with the [Person Profile Endpoint](https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint) with the `use_cache=if-recent` parameter.
        :type enrich_profile: str
        :return: An object of :class:`proxycurl.models.ReverseEmailUrlEnrichResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.ReverseEmailUrlEnrichResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/profile/resolve/email',
            params={
                'work_email': work_email,
                'enrich_profile': enrich_profile,
            },
            data={
            },
            result_class=ReverseEmailUrlEnrichResult
        )

    def lookup_email(
        self,
        callback_url: str,
        linkedin_profile_url: str,
    ) -> ExtractionEmailResult:
        """Work Email Lookup Endpoint
        
                Cost: 3 credits / request.
        Lookup work email address of a LinkedIn Person Profile.

        Email addresses returned are verified to not be role-based or catch-all emails. Email addresses
        returned by our API endpoint come with a 95+% deliverability guarantee

        **Endpoint behavior**

        *This endpoint* **_may not_** *return results immediately.*

        If you provided a webhook in your request parameter, our application will call your webhook with
        the result once. See `Webhook request` below.
        
        :param callback_url: Webhook to notify your application when
            the request has finished processing.
        :type callback_url: str
        :param linkedin_profile_url: Linkedin Profile URL of the person you want to
            extract work email address from.
        :type linkedin_profile_url: str
        :return: An object of :class:`proxycurl.models.ExtractionEmailResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.ExtractionEmailResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/profile/email',
            params={
                'callback_url': callback_url,
                'linkedin_profile_url': linkedin_profile_url,
            },
            data={
            },
            result_class=ExtractionEmailResult
        )

    def personal_contact(
        self,
        linkedin_profile_url: str,
    ) -> PDLPhoneNumberResult:
        """Personal Contact Number Lookup Endpoint
        
                Cost: 1 credit / contact number returned.
        Given an LinkedIn profile, returns a list of personal contact numbers belonging to this identity.
        
        :param linkedin_profile_url: LinkedIn Profile URL of the person you want to extract personal contact numbers from.
        :type linkedin_profile_url: str
        :return: An object of :class:`proxycurl.models.PDLPhoneNumberResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.PDLPhoneNumberResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/contact-api/personal-contact',
            params={
                'linkedin_profile_url': linkedin_profile_url,
            },
            data={
            },
            result_class=PDLPhoneNumberResult
        )

    def personal_email(
        self,
        linkedin_profile_url: str,
        email_validation: str,
    ) -> PDLEmailResult:
        """Personal Email Lookup Endpoint
        
                Cost: 1 credit / email returned.
        Given an LinkedIn profile, returns a list of personal emails belonging to this identity. Emails are verified to be deliverable.
        
        :param linkedin_profile_url: LinkedIn Profile URL of the person you want to extract personal email addresses from.
        :type linkedin_profile_url: str
        :param email_validation: Perform deliverability validation on each email. (Costs 1 extra credit per email found).

            Takes the following values:
             * include - Perform email validation.
             * exclude (default) - Do not perform email validation.
        :type email_validation: str
        :return: An object of :class:`proxycurl.models.PDLEmailResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.PDLEmailResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/contact-api/personal-email',
            params={
                'linkedin_profile_url': linkedin_profile_url,
                'email_validation': email_validation,
            },
            data={
            },
            result_class=PDLEmailResult
        )

    def profile_picture(
        self,
        linkedin_person_profile_url: str,
    ) -> ProfilePicture:
        """Person Profile Picture Endpoint
        
                Cost: 0 credit / successful request.
        Get the profile picture of a person.

        Profile pictures are served from cached people profiles found within [LinkDB](https://nubela.co/proxycurl/linkdb).
        If the profile does not exist within [LinkDB](https://nubela.co/proxycurl/linkdb), then the API will return a `404` status code.
        
        :param linkedin_person_profile_url: LinkedIn Profile URL of the person that you are trying to get the profile picture of.
        :type linkedin_person_profile_url: str
        :return: An object of :class:`proxycurl.models.ProfilePicture` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.ProfilePicture`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/person/profile-picture',
            params={
                'linkedin_person_profile_url': linkedin_person_profile_url,
            },
            data={
            },
            result_class=ProfilePicture
        )

    def person_search(
        self,
        first_name: str,
        last_name: str,
        follower_count_min: str,
        follower_count_max: str,
        occupation: str,
        headline: str,
        summary: str,
        country: str,
        country_full_name: str,
        city: str,
        state: str,
        connections_min: str,
        connections_max: str,
        birth_date_after: str,
        birth_date_before: str,
        page_size: str,
        enrich_profiles: str,
    ) -> PersonSearchResult:
        """Person Search Endpoint
        
                Cost: 35 credits / request.
        Search for people that meet a set of criteria within our exhaustive dataset of people profiles.

        This API endpoint is powered by [LinkDB](https://nubela.co/proxycurl/linkdb), our exhaustive dataset of people and company profiles.
        
        :param first_name: Filter people by their first names by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type first_name: str
        :param last_name: Filter people by their last names by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type last_name: str
        :param follower_count_min: Filter people with a LinkedIn follower count *more than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type follower_count_min: str
        :param follower_count_max: Filter people with a LinkedIn follower count *less than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type follower_count_max: str
        :param occupation: Filter people by their occupations by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type occupation: str
        :param headline: Filter people by their headlines by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type headline: str
        :param summary: Filter people by their summaries by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type summary: str
        :param country: Filter people by their countries (depicted by a 2-letter country code (ISO 3166-1 alpha-2)) by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type country: str
        :param country_full_name: Filter people by their countries (in English words) by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type country_full_name: str
        :param city: Filter people by their cities by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type city: str
        :param state: Filter people by their states by matching it against a regular expression.

            The default value of this parameter is `null`.

            The accepted value is a regular expression (regex).
        :type state: str
        :param connections_min: Filter people with a LinkedIn connection count *more than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type connections_min: str
        :param connections_max: Filter people with a LinkedIn connection count *less than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type connections_max: str
        :param birth_date_after: Filter people with a birth date *more than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type birth_date_after: str
        :param birth_date_before: Filter people with a birth date *less than* a value given in this parameter.

            The default value of this parameter is `null`.
        :type birth_date_before: str
        :param page_size: Tune the maximum results returned per API call.

            The default value of this parameter is `100`.

            Accepted values for this parameter is an integer ranging from `1` to `100`.
        :type page_size: str
        :param enrich_profiles: Get the full profile data of people returned instead of only their LinkedIn profile URLs.

            Each request respond with a streaming response of profiles.

            The valid values are:

            * `skip` (default): lists employee's profile url
            * `enrich`: lists full profile of employees

            Calling this API endpoint with this parameter would add `1` credit per result returned.
        :type enrich_profiles: str
        :return: An object of :class:`proxycurl.models.PersonSearchResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.PersonSearchResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/search/person',
            params={
                'first_name': first_name,
                'last_name': last_name,
                'follower_count_min': follower_count_min,
                'follower_count_max': follower_count_max,
                'occupation': occupation,
                'headline': headline,
                'summary': summary,
                'country': country,
                'country_full_name': country_full_name,
                'city': city,
                'state': state,
                'connections_min': connections_min,
                'connections_max': connections_max,
                'birth_date_after': birth_date_after,
                'birth_date_before': birth_date_before,
                'page_size': page_size,
                'enrich_profiles': enrich_profiles,
            },
            data={
            },
            result_class=PersonSearchResult
        )


class _LinkedinCompany:
    def __init__(self, linkedin):
        self.linkedin = linkedin

    def get(
        self,
        use_cache: str,
        url: str,
        acquisitions: str,
        exit_data: str,
        extra: str,
        funding_data: str,
        categories: str,
        resolve_numeric_id: str,
    ) -> LinkedinCompany:
        """Company Profile Endpoint
        
                Cost: 1 credit / successful request.
        Get structured data of a Company Profile
        
        :param use_cache: `if-present` The default behavior. Fetches profile from cache regardless of age of profile. If profile is not available in cache, API will attempt to source profile externally.

            `if-recent` API will make a best effort to return a fresh profile no older than 29 days.Costs an extra `1` credit on top of the cost of the base endpoint.
        :type use_cache: str
        :param url: URL of the LinkedIn Company Profile to crawl.

            URL should be in the format of `https://www.linkedin.com/company/<public_identifier>`
        :type url: str
        :param acquisitions: Provides further enriched data on acquisitions made by this company from external sources.

            Default value is `"exclude"`.
            The other acceptable value is `"include"`, which will include these acquisition data (if available) for `1` extra credit.
        :type acquisitions: str
        :param exit_data: Returns a list of investment portfolio exits.

            Default value is `"exclude"`.
            The other acceptable value is `"include"`, which will include these categories (if available) for `1` extra credit.
        :type exit_data: str
        :param extra: Enriches the Company Profile with extra details from external sources.
            Details include Crunchbase ranking, contact email, phone number, Facebook account, Twitter account, funding rounds and amount, IPO status, investor information, etc.

            Default value is `"exclude"`.
            The other acceptable value is `"include"`, which will include these extra details (if available) for `1` extra credit.
        :type extra: str
        :param funding_data: Returns a list of funding rounds that this company has received.

            Default value is `"exclude"`.
            The other acceptable value is `"include"`, which will include these categories (if available) for `1` extra credit.
        :type funding_data: str
        :param categories: Appends categories data of this company.

            Default value is `"exclude"`.
            The other acceptable value is `"include"`, which will include these categories (if available) for `1` extra credit.
        :type categories: str
        :param resolve_numeric_id: Enable support for Company Profile URLs with numerical IDs that you most frequently fetch from Sales Navigator.
            We achieve this by resolving numerical IDs into vanity IDs with cached company profiles from [LinkDB](https://nubela.co/proxycurl/linkdb).
            For example, we will turn `https://www.linkedin.com/company/1234567890` to `https://www.linkedin.com/company/acme-corp` -- for which the API endpoint only supports the latter.

            This parameter accepts the following values:
            - `false` (default value) - Will not resolve numerical IDs.
            - `true` - Enable support for Company Profile URLs with numerical IDs.
            Costs an extra `2` credit on top of the base cost of the endpoint.
        :type resolve_numeric_id: str
        :return: An object of :class:`proxycurl.models.LinkedinCompany` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.LinkedinCompany`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company',
            params={
                'use_cache': use_cache,
                'url': url,
                'acquisitions': acquisitions,
                'exit_data': exit_data,
                'extra': extra,
                'funding_data': funding_data,
                'categories': categories,
                'resolve_numeric_id': resolve_numeric_id,
            },
            data={
            },
            result_class=LinkedinCompany
        )

    def resolve(
        self,
        enrich_profile: str,
        company_name: str,
        company_domain: str,
        company_location: str,
    ) -> CompanyUrlEnrichResult:
        """Company Lookup Endpoint
        
                Cost: 2 credits / successful request.
        Resolve Company LinkedIn Profile from company name,
            domain name and location.
        
        :param enrich_profile: Enrich the result with a cached profile of the lookup result.

            The valid values are:

            * `skip` (default): do not enrich the results with cached profile data
            * `enrich`: enriches the result with cached profile data

            Calling this API endpoint with this parameter would add 1 credit.

            If you require [fresh profile data](https://nubela.co/blog/how-fresh-are-profiles-returned-by-proxycurl-api/),
            please chain this API call with the [Company Profile Endpoint](https://nubela.co/proxycurl/docs#company-api-company-profile-endpoint) with the `use_cache=if-recent` parameter.
        :type enrich_profile: str
        :param company_name: Company Name
            Requires either `company_domain` or `company_name`
        :type company_name: str
        :param company_domain: Company website or Company domain
            Requires either `company_domain` or `company_name`
        :type company_domain: str
        :param company_location: The location / region of company.
            ISO 3166-1 alpha-2 codes
        :type company_location: str
        :return: An object of :class:`proxycurl.models.CompanyUrlEnrichResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.CompanyUrlEnrichResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/resolve',
            params={
                'enrich_profile': enrich_profile,
                'company_name': company_name,
                'company_domain': company_domain,
                'company_location': company_location,
            },
            data={
            },
            result_class=CompanyUrlEnrichResult
        )

    def find_job(
        self,
        search_id: str,
        keyword: str,
        geo_id: str,
        flexibility: str,
        when: str,
        experience_level: str,
        job_type: str,
    ) -> JobListPage:
        """Jobs Listing Endpoint
        
                Cost: 2 credits / successful request.
        List jobs posted by a company on LinkedIn
        
        :param search_id: The `search_id` of the company on LinkedIn.
            You can get the `search_id` of a LinkedIn company via
            [Company Profile API](#company-api-company-profile-endpoint).
        :type search_id: str
        :param keyword: The keyword to search for.
        :type keyword: str
        :param geo_id: The `geo_id` of the location to search for.
            For example, `92000000` is the `geo_id` of world wide.

            See [this article](https://nubela.co/blog/how-to-fetch-geo_id-parameter-for-the-job-api/?utm_source=blog&utm_medium=web&utm_campaign=docs-redirect-to-geo_id-article) as to how you may be able to match regions to `geo_id` input values.
        :type geo_id: str
        :param flexibility: The flexibility of the job.
            It accepts the following 3 case insensitive values only:
            - `remote`
            - `on-site`
            - `hybrid`
            - `anything` (default)
        :type flexibility: str
        :param when: The time when the job is posted,
            It accepts the following case-insensitive values only:
            - `yesterday`
            - `past-week`
            - `past-month`
            - `anytime` (default)
        :type when: str
        :param experience_level: The experience level needed for the job.
            It accepts the following 6 case-insensitive values only:
            - `internship`
            - `entry_level`
            - `associate`
            - `mid_senior_level`
            - `director`
            - `anything` (default)
        :type experience_level: str
        :param job_type: The nature of the job.
            It accepts the following 7 case-insensitive values only:
            - `full-time`
            - `part-time`
            - `contract`
            - `internship`
            - `temporary`
            - `volunteer`
            - `anything` (default)
        :type job_type: str
        :return: An object of :class:`proxycurl.models.JobListPage` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.JobListPage`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/v2/linkedin/company/job',
            params={
                'search_id': search_id,
                'keyword': keyword,
                'geo_id': geo_id,
                'flexibility': flexibility,
                'when': when,
                'experience_level': experience_level,
                'job_type': job_type,
            },
            data={
            },
            result_class=JobListPage
        )

    def job_count(
        self,
        search_id: str,
        keyword: str,
        geo_id: str,
        flexibility: str,
        when: str,
        experience_level: str,
        job_type: str,
    ) -> JobListCount:
        """Jobs Listing Count Endpoint
        
                Cost: 2 credits / successful request.
        Count number of jobs posted by a company on LinkedIn
        
        :param search_id: The `search_id` of the company on LinkedIn.
            You can get the `search_id` of a LinkedIn company via
            [Company Profile API](#company-api-company-profile-endpoint).
        :type search_id: str
        :param keyword: The keyword to search for.
        :type keyword: str
        :param geo_id: The `geo_id` of the location to search for.
            For example, `92000000` is the `geo_id` of world wide.

            See [this article](https://nubela.co/blog/how-to-fetch-geo_id-parameter-for-the-job-api/?utm_source=blog&utm_medium=web&utm_campaign=docs-redirect-to-geo_id-article) as to how you may be able to match regions to `geo_id` input values.
        :type geo_id: str
        :param flexibility: The flexibility of the job.
            It accepts the following 3 case insensitive values only:
            - `remote`
            - `on-site`
            - `hybrid`
            - `anything` (default)
        :type flexibility: str
        :param when: The time when the job is posted,
            It accepts the following case-insensitive values only:
            - `yesterday`
            - `past-week`
            - `past-month`
            - `anytime` (default)
        :type when: str
        :param experience_level: The experience level needed for the job.
            It accepts the following 6 case-insensitive values only:
            - `internship`
            - `entry_level`
            - `associate`
            - `mid_senior_level`
            - `director`
            - `anything` (default)
        :type experience_level: str
        :param job_type: The nature of the job.
            It accepts the following 7 case-insensitive values only:
            - `full-time`
            - `part-time`
            - `contract`
            - `internship`
            - `temporary`
            - `volunteer`
            - `anything` (default)
        :type job_type: str
        :return: An object of :class:`proxycurl.models.JobListCount` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.JobListCount`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/v2/linkedin/company/job/count',
            params={
                'search_id': search_id,
                'keyword': keyword,
                'geo_id': geo_id,
                'flexibility': flexibility,
                'when': when,
                'experience_level': experience_level,
                'job_type': job_type,
            },
            data={
            },
            result_class=JobListCount
        )

    def employee_count(
        self,
        url: str,
        employment_status: str,
        linkedin_employee_count: str,
        use_cache: str,
    ) -> EmployeeCount:
        """Employee Count Endpoint
        
                Cost: 1 credit / successful request.
        Get a number of total employees of a Company.

        Get an employee count of this company from various sources.
        
        :param url: URL of the LinkedIn Company Profile to target.

            URL should be in the format of `https://www.linkedin.com/company/<public_identifier>`
        :type url: str
        :param employment_status: Parameter to tell the API to filter past or current employees.

            Valid values are `current`, `past`, and `all`:

            * `current` (default) : count current employees
            * `past` : count past employees
            * `all` : count current & past employees
        :type employment_status: str
        :param linkedin_employee_count: Option to include a scraped employee count value from the target company's LinkedIn profile.

            Valid values are `include` and `exclude`:

            * `exclude` (default) : To exclude the scraped employee count.
            * `include` : To include the scraped employee count.

            Costs an extra `1` credit on top of the base cost of the endpoint.
        :type linkedin_employee_count: str
        :param use_cache: `if-present`: The default behavior. Fetches data from LinkDB cache regardless of age of profile.

            `if-recent`: API will make a best effort to return a fresh data no older than 29 days. Costs an extra 1 credit on top of the cost of the base endpoint.
        :type use_cache: str
        :return: An object of :class:`proxycurl.models.EmployeeCount` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.EmployeeCount`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/employees/count',
            params={
                'url': url,
                'employment_status': employment_status,
                'linkedin_employee_count': linkedin_employee_count,
                'use_cache': use_cache,
            },
            data={
            },
            result_class=EmployeeCount
        )

    def employee_list(
        self,
        url: str,
        resolve_numeric_id: str,
        sort_by: str,
        employment_status: str,
        page_size: str,
        role_search: str,
        enrich_profiles: str,
        country: str,
    ) -> EmployeeList:
        """Employee Listing Endpoint
        
                Cost: 3 credits / employee returned.
        Get a list of employees of a Company.

        This API endpoint is limited by LinkDB which is populated with profiles in the US, UK, Canada, Israel, Australia, Ireland, New Zealand and Singapore.
        As such, this endpoint is best used to list employees working in companies based in those locations only.
        
        :param url: URL of the LinkedIn Company Profile to target.

            URL should be in the format of `https://www.linkedin.com/company/<public_identifier>`
        :type url: str
        :param resolve_numeric_id: Enable support for Company Profile URLs with numerical IDs that you most frequently fetch from Sales Navigator. 
            We achieve this by resolving numerical IDs into vanity IDs with cached company profiles from [LinkDB](https://nubela.co/proxycurl/linkdb). 
            For example, we will turn `https://www.linkedin.com/company/1234567890` to `https://www.linkedin.com/company/acme-corp` -- for which the API endpoint only supports the latter.

            This parameter accepts the following values:
            - `false` (default value) - Will not resolve numerical IDs.
            - `true` - Enable support for Company Profile URLs with numerical IDs. 
            Costs an extra `2` credit on top of the base cost of the endpoint.
        :type resolve_numeric_id: str
        :param sort_by: Sort employees by recency.

            Valid values are:
            * `recently-joined` - Sort employees by their join date. The most recent employee is on the top of the list.
            * `recently-left` - Sort employees by their departure date. The most recent employee who had just left is on the top of this list.
            * `none` - The default value. Do not sort.

            If this parameter is supplied with a value other than `none`, will add `50` credits to the base cost of the API endpoint regardless number of results returned. It will also add an additional cost of `10` credits per employee returned.
        :type sort_by: str
        :param employment_status: Parameter to tell the API to return past or current employees.

            Valid values are `current`, `past`, and `all`:

            * `current` (default) : lists current employees
            * `past` : lists past employees
            * `all` : lists current & past employees
        :type employment_status: str
        :param page_size: Tune the maximum results returned per API call.

            The default value of this parameter is `200000`.

            Accepted values for this parameter is an integer ranging from `1` to `200000`.

            When `enrich_profiles=enrich`, this parameter accepts value ranging from `1` to `100`.
        :type page_size: str
        :param role_search: Filter employees by their title by matching the employee's title against a *regular expression*.

            The default value of this parameter is `null`.

            The accepted value is a *regular expression* (regex).

            (The base cost of calling this API endpoint with this parameter would be `10` credits.
            Each employee matched and returned would cost `6` credits per employee returned.)
        :type role_search: str
        :param enrich_profiles: Get the full profile of employees instead of only their profile urls.

            Each request respond with a streaming response of profiles.

            The valid values are:

            * `skip` (default): lists employee's profile url
            * `enrich`: lists full profile of employees

            Calling this API endpoint with this parameter would add `1` credit per employee returned.
        :type enrich_profiles: str
        :param country: Limit the result set to the country locality of the profile. For example, set the parameter of `country=us` if you only want profiles from the US.

            This parameter accepts a **case-insensitive** [Alpha-2 ISO3166 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

            Costs an extra `3` credit per result returned.
        :type country: str
        :return: An object of :class:`proxycurl.models.EmployeeList` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.EmployeeList`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/employees',
            params={
                'url': url,
                'resolve_numeric_id': resolve_numeric_id,
                'sort_by': sort_by,
                'employment_status': employment_status,
                'page_size': page_size,
                'role_search': role_search,
                'enrich_profiles': enrich_profiles,
                'country': country,
            },
            data={
            },
            result_class=EmployeeList
        )

    def role_lookup(
        self,
        company_name: str,
        role: str,
        enrich_profile: str,
    ) -> RoleSearchErichedResult:
        """Role Lookup Endpoint
        
                Cost: 3 credits / successful request.
        Finds the closest (person) profile with a given role in a Company.
        For example, you can use this endpoint to find the "CTO" of "Apple".
        This API endpoint returns only one result that is the closest match.

        There is also the [Employee Search Endpoint]
        (https://nubela.co/proxycurl/docs#company-api-employee-search-api-endpoint)
         which is powered by [LinkDB](https://nubela.co/proxycurl/linkdb) if you
         require:

        * precision on the target company
        * a list of employees that matches a role (instead of one result).
        
        :param company_name: Name of the company that you are searching for
        :type company_name: str
        :param role: Role of the profile that you are lookin up
        :type role: str
        :param enrich_profile: Enrich the result with a cached profile of the lookup result.

            The valid values are:

            * `skip` (default): do not enrich the results with cached profile data
            * `enrich`: enriches the result with cached profile data

            Calling this API endpoint with this parameter would add 1 credit.

            If you require [fresh profile data](https://nubela.co/blog/how-fresh-are-profiles-returned-by-proxycurl-api/),
            please chain this API call with the [Person Profile Endpoint](https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint) with the `use_cache=if-recent` parameter.
        :type enrich_profile: str
        :return: An object of :class:`proxycurl.models.RoleSearchErichedResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.RoleSearchErichedResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/find/company/role',
            params={
                'company_name': company_name,
                'role': role,
                'enrich_profile': enrich_profile,
            },
            data={
            },
            result_class=RoleSearchErichedResult
        )

    def reveal(
        self,
        ip: str,
        role: str,
        role_personal_email: str,
        role_contact_number: str,
    ) -> CompanyReveal:
        """Reveal Endpoint
        
                Cost: 2 credits / successful request.
        Deanonymize an IPv4 address and associate the Company behind the IPv4 address.
        
        :param ip: The target IPv4 address.
        :type ip: str
        :param role: Lookup and append an employee of a certain role of the company.
            Within the same API call, You can choose to lookup a person with a given role within this organisation that you might want to reach out to.
        :type role: str
        :param role_personal_email: Append personal email addresses to the response if the system finds a relevant person profile.
        :type role_personal_email: str
        :param role_contact_number: Append personal contact numbers to the response if the system finds a relevant person profile.
        :type role_contact_number: str
        :return: An object of :class:`proxycurl.models.CompanyReveal` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.CompanyReveal`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/reveal/company',
            params={
                'ip': ip,
                'role': role,
                'role_personal_email': role_personal_email,
                'role_contact_number': role_contact_number,
            },
            data={
            },
            result_class=CompanyReveal
        )

    def employees(
        self,
        url: str,
        resolve_numeric_id: str,
        sort_by: str,
        employment_status: str,
        page_size: str,
        role_search: str,
        enrich_profiles: str,
        country: str,
    ) -> EmployeeList:
        """Employee Listing Endpoint
        
                Cost: 3 credits / employee returned.
        Get a list of employees of a Company.

        This API endpoint is limited by LinkDB which is populated with profiles in the US, UK, Canada, Israel, Australia, Ireland, New Zealand and Singapore.
        As such, this endpoint is best used to list employees working in companies based in those locations only.
        
        :param url: URL of the LinkedIn Company Profile to target.

            URL should be in the format of `https://www.linkedin.com/company/<public_identifier>`
        :type url: str
        :param resolve_numeric_id: Enable support for Company Profile URLs with numerical IDs that you most frequently fetch from Sales Navigator. 
            We achieve this by resolving numerical IDs into vanity IDs with cached company profiles from [LinkDB](https://nubela.co/proxycurl/linkdb). 
            For example, we will turn `https://www.linkedin.com/company/1234567890` to `https://www.linkedin.com/company/acme-corp` -- for which the API endpoint only supports the latter.

            This parameter accepts the following values:
            - `false` (default value) - Will not resolve numerical IDs.
            - `true` - Enable support for Company Profile URLs with numerical IDs. 
            Costs an extra `2` credit on top of the base cost of the endpoint.
        :type resolve_numeric_id: str
        :param sort_by: Sort employees by recency.

            Valid values are:
            * `recently-joined` - Sort employees by their join date. The most recent employee is on the top of the list.
            * `recently-left` - Sort employees by their departure date. The most recent employee who had just left is on the top of this list.
            * `none` - The default value. Do not sort.

            If this parameter is supplied with a value other than `none`, will add `50` credits to the base cost of the API endpoint regardless number of results returned. It will also add an additional cost of `10` credits per employee returned.
        :type sort_by: str
        :param employment_status: Parameter to tell the API to return past or current employees.

            Valid values are `current`, `past`, and `all`:

            * `current` (default) : lists current employees
            * `past` : lists past employees
            * `all` : lists current & past employees
        :type employment_status: str
        :param page_size: Tune the maximum results returned per API call.

            The default value of this parameter is `200000`.

            Accepted values for this parameter is an integer ranging from `1` to `200000`.

            When `enrich_profiles=enrich`, this parameter accepts value ranging from `1` to `100`.
        :type page_size: str
        :param role_search: Filter employees by their title by matching the employee's title against a *regular expression*.

            The default value of this parameter is `null`.

            The accepted value is a *regular expression* (regex).

            (The base cost of calling this API endpoint with this parameter would be `10` credits.
            Each employee matched and returned would cost `6` credits per employee returned.)
        :type role_search: str
        :param enrich_profiles: Get the full profile of employees instead of only their profile urls.

            Each request respond with a streaming response of profiles.

            The valid values are:

            * `skip` (default): lists employee's profile url
            * `enrich`: lists full profile of employees

            Calling this API endpoint with this parameter would add `1` credit per employee returned.
        :type enrich_profiles: str
        :param country: Limit the result set to the country locality of the profile. For example, set the parameter of `country=us` if you only want profiles from the US.

            This parameter accepts a **case-insensitive** [Alpha-2 ISO3166 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

            Costs an extra `3` credit per result returned.
        :type country: str
        :return: An object of :class:`proxycurl.models.EmployeeList` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.EmployeeList`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/employees',
            params={
                'url': url,
                'resolve_numeric_id': resolve_numeric_id,
                'sort_by': sort_by,
                'employment_status': employment_status,
                'page_size': page_size,
                'role_search': role_search,
                'enrich_profiles': enrich_profiles,
                'country': country,
            },
            data={
            },
            result_class=EmployeeList
        )

    def employee_search(
        self,
        resolve_numeric_id: str,
        enrich_profiles: str,
        country: str,
        keyword_regex: str,
        linkedin_company_profile_url: str,
        page_size: str,
    ) -> EmployeeList:
        """Employee Search Endpoint
        
                Cost: 10 credits / successful request.
        Search employees of a target by their job title.
        This API endpoint is syntactic sugar for the role_search parameter under the [Employee Listing Endpoint](https://nubela.co/proxycurl/docs#company-api-employee-listing-endpoint).

        Results are limited by data that we have within [LinkDB](https://nubela.co/proxycurl/linkdb).
        Use [Role Lookup API Endpoint](https://nubela.co/proxycurl/docs#people-api-role-lookup-endpoint) if you need to query for profiles without LinkDB constraints.
        The drawbacks of the Role Lookup API Endpoint is that it is less precise and can return at most one result per query.
        
        :param resolve_numeric_id: Enable support for Company Profile URLs with numerical IDs that you most frequently fetch from Sales Navigator. 
            We achieve this by resolving numerical IDs into vanity IDs with cached company profiles from [LinkDB](https://nubela.co/proxycurl/linkdb). 
            For example, we will turn `https://www.linkedin.com/company/1234567890` to `https://www.linkedin.com/company/acme-corp` -- for which the API endpoint only supports the latter.

            This parameter accepts the following values:
            - `false` (default value) - Will not resolve numerical IDs.
            - `true` - Enable support for Company Profile URLs with numerical IDs. 
            Costs an extra `2` credit on top of the base cost of the endpoint.
        :type resolve_numeric_id: str
        :param enrich_profiles: Get the full profile of employees instead of only their profile urls.

            Each request respond with a streaming response of profiles.

            The valid values are:

            * `skip` (default): lists employee's profile url
            * `enrich`: lists full profile of employees

            Calling this API endpoint with this parameter would add `1` credit per employee returned.
        :type enrich_profiles: str
        :param country: Limit the result set to the country locality of the profile. For example, set the parameter of `country=us` if you only want profiles from the US.

            This parameter accepts a **case-insensitive** [Alpha-2 ISO3166 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

            Costs an extra `3` credit per result returned.
        :type country: str
        :param keyword_regex: Job title keyword to search for in regular expression format.
        :type keyword_regex: str
        :param linkedin_company_profile_url: LinkedIn Profile URL of the target company.
        :type linkedin_company_profile_url: str
        :param page_size: Tune the maximum results returned per API call.
            The default value of this parameter is `200000`.
            Accepted values for this parameter is an integer ranging from `1` to `200000`.
        :type page_size: str
        :return: An object of :class:`proxycurl.models.EmployeeList` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.EmployeeList`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/employee/search',
            params={
                'resolve_numeric_id': resolve_numeric_id,
                'enrich_profiles': enrich_profiles,
                'country': country,
                'keyword_regex': keyword_regex,
                'linkedin_company_profile_url': linkedin_company_profile_url,
                'page_size': page_size,
            },
            data={
            },
            result_class=EmployeeList
        )

    def profile_picture(
        self,
        linkedin_company_profile_url: str,
    ) -> ProfilePicture:
        """Company Profile Picture Endpoint
        
                Cost: 0 credit / successful request.
        Get the profile picture of a company.

        Profile pictures are served from cached company profiles found within [LinkDB](https://nubela.co/proxycurl/linkdb).
        If the profile does not exist within [LinkDB](https://nubela.co/proxycurl/linkdb), then the API will return a `404` status code.
        
        :param linkedin_company_profile_url: LinkedIn Profile URL of the company that you are trying to get the profile picture of.
        :type linkedin_company_profile_url: str
        :return: An object of :class:`proxycurl.models.ProfilePicture` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.ProfilePicture`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/company/profile-picture',
            params={
                'linkedin_company_profile_url': linkedin_company_profile_url,
            },
            data={
            },
            result_class=ProfilePicture
        )

    def find_role(
        self,
        company_name: str,
        role: str,
        enrich_profile: str,
    ) -> RoleSearchErichedResult:
        """Role Lookup Endpoint
        
                Cost: 3 credits / successful request.
        Finds the closest (person) profile with a given role in a Company.
        For example, you can use this endpoint to find the "CTO" of "Apple".
        This API endpoint returns only one result that is the closest match.

        There is also the [Employee Search Endpoint]
        (https://nubela.co/proxycurl/docs#company-api-employee-search-api-endpoint)
         which is powered by [LinkDB](https://nubela.co/proxycurl/linkdb) if you
         require:

        * precision on the target company
        * a list of employees that matches a role (instead of one result).
        
        :param company_name: Name of the company that you are searching for
        :type company_name: str
        :param role: Role of the profile that you are lookin up
        :type role: str
        :param enrich_profile: Enrich the result with a cached profile of the lookup result.

            The valid values are:

            * `skip` (default): do not enrich the results with cached profile data
            * `enrich`: enriches the result with cached profile data

            Calling this API endpoint with this parameter would add 1 credit.

            If you require [fresh profile data](https://nubela.co/blog/how-fresh-are-profiles-returned-by-proxycurl-api/),
            please chain this API call with the [Person Profile Endpoint](https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint) with the `use_cache=if-recent` parameter.
        :type enrich_profile: str
        :return: An object of :class:`proxycurl.models.RoleSearchErichedResult` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.RoleSearchErichedResult`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/find/company/role',
            params={
                'company_name': company_name,
                'role': role,
                'enrich_profile': enrich_profile,
            },
            data={
            },
            result_class=RoleSearchErichedResult
        )


class _LinkedinSchool:
    def __init__(self, linkedin):
        self.linkedin = linkedin

    def get(
        self,
        use_cache: str,
        url: str,
    ) -> LinkedinSchool:
        """School Profile Endpoint
        
                Cost: 1 credit / successful request.
        Get structured data of a LinkedIn School Profile
        
        :param use_cache: `if-present` The default behavior. Fetches profile from cache regardless of age of profile. If profile is not available in cache, API will attempt to source profile externally.

            `if-recent` API will make a best effort to return a fresh profile no older than 29 days.Costs an extra `1` credit on top of the cost of the base endpoint.
        :type use_cache: str
        :param url: URL of the LinkedIn School Profile to crawl.

            URL should be in the format of `https://www.linkedin.com/school/<public_identifier>`
        :type url: str
        :return: An object of :class:`proxycurl.models.LinkedinSchool` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.LinkedinSchool`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/school',
            params={
                'use_cache': use_cache,
                'url': url,
            },
            data={
            },
            result_class=LinkedinSchool
        )

    def students(
        self,
        linkedin_school_url: str,
        resolve_numeric_id: str,
        sort_by: str,
        student_status: str,
        page_size: str,
        search_keyword: str,
        enrich_profiles: str,
        country: str,
    ) -> StudentList:
        """Student Listing Endpoint
        
                Cost: 3 credits / student returned.
        Get a list of students of a school or university.
        
        :param linkedin_school_url: URL of the LinkedIn School Profile to target.

            URL should be in the format of `https://www.linkedin.com/school/<public_identifier>`
        :type linkedin_school_url: str
        :param resolve_numeric_id: Enable support for School Profile URLs with numerical IDs that you most frequently fetch from Sales Navigator. 
            We achieve this by resolving numerical IDs into vanity IDs with cached company profiles from [LinkDB](https://nubela.co/proxycurl/linkdb). 
            For example, we will turn `https://www.linkedin.com/school/1234567890` to `https://www.linkedin.com/school/acme-corp` -- for which the API endpoint only supports the latter.

            This parameter accepts the following values:
            - `false` (default value) - Will not resolve numerical IDs.
            - `true` - Enable support for School Profile URLs with numerical IDs. 
            Costs an extra `2` credit on top of the base cost of the endpoint.
        :type resolve_numeric_id: str
        :param sort_by: Sort students by matriculation or graduation dates.

            Valid values are:
            * `recently-matriculated` - Sort students by their matriculation date. Students who had had most recently started school is on the top of the list.
            * `recently-graduated` - Sort students by their graduation date. The most recently graduated student is on the top of this list.
            * `none` - The default value. Do not sort.

            If this parameter is supplied with a value other than `none`, will add `50` credits to the base cost of the API endpoint regardless number of results returned. It will also add an additional cost of `10` credits per student returned.
        :type sort_by: str
        :param student_status: Parameter to tell the API to return past or current students.

            Valid values are `current`, `past`, and `all`:

            * `current` (default) : lists current students
            * `past` : lists past students
            * `all` : lists current & past students
        :type student_status: str
        :param page_size: Tune the maximum results returned per API call.

            The default value of this parameter is `200000`.

            Accepted values for this parameter is an integer ranging from `1` to `200000`.

            When `enrich_profiles=enrich`, this parameter accepts value ranging from `1` to `100`.
        :type page_size: str
        :param search_keyword: Filter students by their major by matching the student's major against a *regular expression*.

            The default value of this parameter is `null`.

            The accepted value is a *regular expression* (regex).

            (The base cost of calling this API endpoint with this parameter would be `10` credits.
            Each student matched and returned would cost `6` credits per student returned.)
        :type search_keyword: str
        :param enrich_profiles: Get the full profile of students instead of only their profile urls.

            Each request respond with a streaming response of profiles.

            The valid values are:

            * `skip` (default): lists student's profile url
            * `enrich`: lists full profile of students

            *Calling this API endpoint with this parameter would add `1` credit per student returned.*
        :type enrich_profiles: str
        :param country: Limit the result set to the country locality of the profile. For example, set the parameter of `country=us` if you only want profiles from the US.

            This parameter accepts a **case-insensitive** [Alpha-2 ISO3166 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

            Costs an extra `3` credit per result returned.
        :type country: str
        :return: An object of :class:`proxycurl.models.StudentList` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.StudentList`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/school/students',
            params={
                'linkedin_school_url': linkedin_school_url,
                'resolve_numeric_id': resolve_numeric_id,
                'sort_by': sort_by,
                'student_status': student_status,
                'page_size': page_size,
                'search_keyword': search_keyword,
                'enrich_profiles': enrich_profiles,
                'country': country,
            },
            data={
            },
            result_class=StudentList
        )


class _LinkedinJob:
    def __init__(self, linkedin):
        self.linkedin = linkedin

    def get(
        self,
        url: str,
    ) -> JobProfile:
        """Job Profile Endpoint
        
                Cost: 2 credits / successful request.
        Get structured data of a LinkedIn Job Profile
        
        :param url: URL of the LinkedIn Job Profile to target.

            URL should be in the format of
            `https://www.linkedin.com/jobs/view/<job_id>`.
            [Jobs Listing Endpoint](#jobs-api-jobs-listing-endpoint)
            can be used to retrieve a job URL.
        :type url: str
        :return: An object of :class:`proxycurl.models.JobProfile` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.JobProfile`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/linkedin/job',
            params={
                'url': url,
            },
            data={
            },
            result_class=JobProfile
        )


class _Linkedin:
    person: _LinkedinPerson
    company: _LinkedinCompany
    school: _LinkedinSchool
    job: _LinkedinJob

    def __init__(self, proxycurl):
        self.proxycurl = proxycurl
        self.person = _LinkedinPerson(self)
        self.company = _LinkedinCompany(self)
        self.school = _LinkedinSchool(self)
        self.job = _LinkedinJob(self)


class Proxycurl(ProxycurlBase):
    linkedin: _Linkedin

    def __init__(
        self,
        api_key: str = PROXYCURL_API_KEY,
        base_url: str = BASE_URL,
        timeout: int = TIMEOUT,
        max_retries: int = MAX_RETRIES,
        max_backoff_seconds: int = MAX_BACKOFF_SECONDS
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_backoff_seconds = max_backoff_seconds
        self.linkedin = _Linkedin(self)

    def get_balance(
        self,
    ) -> CreditBalance:
        """View Credit Balance Endpoint
        
                Cost: 0 credit / successful request.
        Get your current credit(s) balance
        
        :return: An object of :class:`proxycurl.models.CreditBalance` or **None** if there is an error.
        :rtype: :class:`proxycurl.models.CreditBalance`
        :raise ProxycurlException: Every error will raise a :class:`proxycurl.gevent.ProxycurlException`

        """

        return self.linkedin.proxycurl.request(
            method='GET',
            url='/proxycurl/api/credit-balance',
            params={
            },
            data={
            },
            result_class=CreditBalance
        )
