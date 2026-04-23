"""Tests for the date dimension generator."""

from __future__ import annotations

from datetime import date

import pytest

from healthsim.dimensional import generate_dim_date


class TestGenerateDimDate:
    """Test suite for generate_dim_date function."""

    def test_correct_row_count_for_date_range(self):
        """Test that correct number of rows are generated for date range."""
        # 2024 is a leap year - should have 366 days
        df = generate_dim_date("2024-01-01", "2024-12-31")
        assert len(df) == 366

        # 2023 is not a leap year - should have 365 days
        df = generate_dim_date("2023-01-01", "2023-12-31")
        assert len(df) == 365

        # Specific range
        df = generate_dim_date("2024-01-01", "2024-01-31")
        assert len(df) == 31

    def test_date_key_format(self):
        """Test that date_key is in YYYYMMDD format."""
        df = generate_dim_date("2024-01-01", "2024-01-03")

        assert df.iloc[0]["date_key"] == 20240101
        assert df.iloc[1]["date_key"] == 20240102
        assert df.iloc[2]["date_key"] == 20240103

    def test_date_key_boundaries(self):
        """Test date keys at year boundaries."""
        df = generate_dim_date("2024-12-30", "2025-01-02")

        assert df.iloc[0]["date_key"] == 20241230
        assert df.iloc[1]["date_key"] == 20241231
        assert df.iloc[2]["date_key"] == 20250101
        assert df.iloc[3]["date_key"] == 20250102

    def test_all_columns_present(self):
        """Test that all required columns are present."""
        df = generate_dim_date("2024-01-01", "2024-01-01")

        expected_columns = [
            "date_key",
            "full_date",
            "year",
            "quarter",
            "month",
            "day",
            "day_of_week",
            "day_of_year",
            "week_of_year",
            "day_name",
            "month_name",
            "quarter_name",
            "year_month",
            "year_quarter",
            "is_weekend",
            "is_month_start",
            "is_month_end",
            "is_quarter_start",
            "is_quarter_end",
            "is_year_start",
            "is_year_end",
            "is_us_federal_holiday",
            "holiday_name",
        ]

        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"

    def test_date_values(self):
        """Test date attribute values."""
        df = generate_dim_date("2024-06-15", "2024-06-15")
        row = df.iloc[0]

        assert row["full_date"] == date(2024, 6, 15)
        assert row["year"] == 2024
        assert row["quarter"] == 2
        assert row["month"] == 6
        assert row["day"] == 15
        assert row["day_of_week"] == 6  # Saturday (ISO: 1=Mon, 7=Sun)
        assert row["day_of_year"] == 167
        assert row["day_name"] == "Saturday"
        assert row["month_name"] == "June"
        assert row["quarter_name"] == "Q2"
        assert row["year_month"] == "2024-06"
        assert row["year_quarter"] == "2024-Q2"

    def test_weekend_flags(self):
        """Test weekend flags are correct."""
        # 2024-01-06 is Saturday, 2024-01-07 is Sunday
        df = generate_dim_date("2024-01-05", "2024-01-08")

        # Friday
        assert df.iloc[0]["is_weekend"] == False  # noqa: E712
        # Saturday
        assert df.iloc[1]["is_weekend"] == True  # noqa: E712
        # Sunday
        assert df.iloc[2]["is_weekend"] == True  # noqa: E712
        # Monday
        assert df.iloc[3]["is_weekend"] == False  # noqa: E712

    def test_month_boundary_flags(self):
        """Test month start/end flags."""
        df = generate_dim_date("2024-01-30", "2024-02-02")

        # Jan 30
        assert df.iloc[0]["is_month_start"] == False  # noqa: E712
        assert df.iloc[0]["is_month_end"] == False  # noqa: E712
        # Jan 31
        assert df.iloc[1]["is_month_start"] == False  # noqa: E712
        assert df.iloc[1]["is_month_end"] == True  # noqa: E712
        # Feb 1
        assert df.iloc[2]["is_month_start"] == True  # noqa: E712
        assert df.iloc[2]["is_month_end"] == False  # noqa: E712

    def test_quarter_boundary_flags(self):
        """Test quarter start/end flags."""
        # Q1 -> Q2 boundary
        df = generate_dim_date("2024-03-31", "2024-04-01")

        # Mar 31 (end of Q1)
        assert df.iloc[0]["is_quarter_start"] == False  # noqa: E712
        assert df.iloc[0]["is_quarter_end"] == True  # noqa: E712
        # Apr 1 (start of Q2)
        assert df.iloc[1]["is_quarter_start"] == True  # noqa: E712
        assert df.iloc[1]["is_quarter_end"] == False  # noqa: E712

    def test_year_boundary_flags(self):
        """Test year start/end flags."""
        df = generate_dim_date("2024-12-31", "2025-01-01")

        # Dec 31
        assert df.iloc[0]["is_year_start"] == False  # noqa: E712
        assert df.iloc[0]["is_year_end"] == True  # noqa: E712
        # Jan 1
        assert df.iloc[1]["is_year_start"] == True  # noqa: E712
        assert df.iloc[1]["is_year_end"] == False  # noqa: E712

    def test_us_federal_holidays_2024(self):
        """Test that US federal holidays are identified correctly for 2024."""
        df = generate_dim_date("2024-01-01", "2024-12-31")
        holidays = df[df["is_us_federal_holiday"]]

        # 2024 should have 11 federal holidays
        assert len(holidays) >= 11

        # Check specific holidays
        holiday_names = set(holidays["holiday_name"].tolist())
        expected = {
            "New Year's Day",
            "Martin Luther King Jr. Day",
            "Presidents Day",
            "Memorial Day",
            "Juneteenth",
            "Independence Day",
            "Labor Day",
            "Columbus Day",
            "Veterans Day",
            "Thanksgiving",
            "Christmas Day",
        }
        assert expected == holiday_names

    def test_christmas_2024_not_observed_different_day(self):
        """Test that Christmas 2024 (Wednesday) is not observed on a different day."""
        df = generate_dim_date("2024-12-24", "2024-12-26")

        christmas = df[df["date_key"] == 20241225].iloc[0]
        assert christmas["holiday_name"] == "Christmas Day"
        assert christmas["is_us_federal_holiday"] == True  # noqa: E712

        # Dec 24 and 26 should not be holidays
        assert df.iloc[0]["is_us_federal_holiday"] == False  # noqa: E712
        assert df.iloc[2]["is_us_federal_holiday"] == False  # noqa: E712

    def test_observed_holiday_saturday(self):
        """Test that holidays on Saturday are observed on Friday."""
        # Independence Day 2026 is Saturday - observed Friday July 3
        df = generate_dim_date("2026-07-02", "2026-07-05")

        # July 3 (Friday) should be the observed holiday
        july_3 = df[df["date_key"] == 20260703].iloc[0]
        assert july_3["holiday_name"] == "Independence Day"
        assert july_3["is_us_federal_holiday"] == True  # noqa: E712

    def test_observed_holiday_sunday(self):
        """Test that holidays on Sunday are observed on Monday."""
        # Christmas 2022 was Sunday - observed Monday Dec 26
        df = generate_dim_date("2022-12-24", "2022-12-27")

        # Dec 26 (Monday) should be the observed holiday
        dec_26 = df[df["date_key"] == 20221226].iloc[0]
        assert dec_26["holiday_name"] == "Christmas Day"
        assert dec_26["is_us_federal_holiday"] == True  # noqa: E712

    def test_mlk_day_third_monday(self):
        """Test MLK Day is third Monday of January."""
        df = generate_dim_date("2024-01-01", "2024-01-31")
        mlk = df[df["holiday_name"] == "Martin Luther King Jr. Day"]

        assert len(mlk) == 1
        mlk_date = mlk.iloc[0]
        assert mlk_date["date_key"] == 20240115  # Jan 15, 2024
        assert mlk_date["day_of_week"] == 1  # Monday

    def test_thanksgiving_fourth_thursday(self):
        """Test Thanksgiving is fourth Thursday of November."""
        df = generate_dim_date("2024-11-01", "2024-11-30")
        thanksgiving = df[df["holiday_name"] == "Thanksgiving"]

        assert len(thanksgiving) == 1
        tg_date = thanksgiving.iloc[0]
        assert tg_date["date_key"] == 20241128  # Nov 28, 2024
        assert tg_date["day_of_week"] == 4  # Thursday

    def test_memorial_day_last_monday(self):
        """Test Memorial Day is last Monday of May."""
        df = generate_dim_date("2024-05-01", "2024-05-31")
        memorial = df[df["holiday_name"] == "Memorial Day"]

        assert len(memorial) == 1
        mem_date = memorial.iloc[0]
        assert mem_date["date_key"] == 20240527  # May 27, 2024
        assert mem_date["day_of_week"] == 1  # Monday

    def test_accepts_date_objects(self):
        """Test that date objects are accepted as inputs."""
        df = generate_dim_date(date(2024, 1, 1), date(2024, 1, 31))
        assert len(df) == 31

    def test_invalid_date_range_raises_error(self):
        """Test that start > end raises ValueError."""
        with pytest.raises(ValueError):
            generate_dim_date("2024-12-31", "2024-01-01")

    def test_single_day_range(self):
        """Test single day range works."""
        df = generate_dim_date("2024-06-15", "2024-06-15")
        assert len(df) == 1

    def test_iso_week_number(self):
        """Test ISO week number calculation."""
        # 2024-01-01 is Monday, ISO week 1
        df = generate_dim_date("2024-01-01", "2024-01-01")
        assert df.iloc[0]["week_of_year"] == 1

        # 2023-12-31 is Sunday, still ISO week 52 of 2023
        df = generate_dim_date("2023-12-31", "2023-12-31")
        assert df.iloc[0]["week_of_year"] == 52

    def test_iso_day_of_week(self):
        """Test ISO day of week (1=Monday, 7=Sunday)."""
        # 2024-01-01 is Monday
        df = generate_dim_date("2024-01-01", "2024-01-07")

        assert df.iloc[0]["day_of_week"] == 1  # Monday
        assert df.iloc[1]["day_of_week"] == 2  # Tuesday
        assert df.iloc[2]["day_of_week"] == 3  # Wednesday
        assert df.iloc[3]["day_of_week"] == 4  # Thursday
        assert df.iloc[4]["day_of_week"] == 5  # Friday
        assert df.iloc[5]["day_of_week"] == 6  # Saturday
        assert df.iloc[6]["day_of_week"] == 7  # Sunday

    def test_leap_year_feb_29(self):
        """Test February 29 in leap year."""
        df = generate_dim_date("2024-02-28", "2024-03-01")

        assert len(df) == 3
        assert df.iloc[0]["date_key"] == 20240228
        assert df.iloc[1]["date_key"] == 20240229  # Leap day
        assert df.iloc[2]["date_key"] == 20240301

        # Feb 29 should be end of month (in Feb)
        assert df.iloc[0]["is_month_end"] == False  # noqa: E712
        assert df.iloc[1]["is_month_end"] == True  # noqa: E712
        assert df.iloc[2]["is_month_start"] == True  # noqa: E712
