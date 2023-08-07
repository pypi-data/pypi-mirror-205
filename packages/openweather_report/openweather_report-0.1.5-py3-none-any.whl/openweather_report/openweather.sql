-- name: save_json_data!
-- Insert json data.
insert into weather.raw_json_data (
         entry_date
        ,api_call
        ,raw_data
        ,software_version
)
values (
         :entry_date
        ,:api_call
        ,:raw_data
        ,:software_version
);

-- name: save_json_data_no_schema!
-- Insert json data.
insert into raw_json_data (
         entry_date
        ,api_call
        ,raw_data
        ,software_version
)
values (
         :entry_date
        ,:api_call
        ,:raw_data
        ,:software_version
);
