-- =============================================================================
-- FILE: BLOOD_BANK_PKG_SPEC_AND_BODY.sql
-- SCHEMA: U310482025_SALAH_SBB_DB
-- =============================================================================

SET SERVEROUTPUT ON;

-- 1. Package Specification (Header)
CREATE OR REPLACE PACKAGE BLOOD_BANK_PKG AS
    -- Function to check if a donor is eligible to donate based on last donation date
    FUNCTION Check_Donor_Eligibility(p_donor_id IN NUMBER) RETURN VARCHAR2;

    -- Procedure to process lab tests and update blood unit status
    PROCEDURE Process_Lab_Test(
        p_barcode_id IN VARCHAR2,
        p_hiv IN VARCHAR2,
        p_hep_b IN VARCHAR2,
        p_hep_c IN VARCHAR2,
        p_syphilis IN VARCHAR2
    );
END BLOOD_BANK_PKG;
/

-- 2. Package Body (Implementation)
CREATE OR REPLACE PACKAGE BODY BLOOD_BANK_PKG AS

    -- Implementation of Check_Donor_Eligibility function
    FUNCTION Check_Donor_Eligibility(p_donor_id IN NUMBER) RETURN VARCHAR2 IS
        v_last_date DATE;
        v_days_passed NUMBER;
    BEGIN
        -- Fetch the last donation date of the given donor
        SELECT Last_Donation_Date INTO v_last_date FROM Donors WHERE Donor_ID = p_donor_id;

        -- If donor has never donated before, they are eligible
        IF v_last_date IS NULL THEN
            RETURN 'ELIGIBLE';
        END IF;

        -- Calculate days passed since last donation
        v_days_passed := SYSDATE - v_last_date;

        -- In many medical standards, 56 days is the minimum duration required between donations
        IF v_days_passed >= 56 THEN
            RETURN 'ELIGIBLE';
        END IF;

        RETURN 'NOT ELIGIBLE (Requires ' || CEIL(56 - v_days_passed) || ' more days)';
    EXCEPTION
        -- Handle exception if the donor ID does not exist in the database
        WHEN NO_DATA_FOUND THEN
            RETURN 'ERROR: Donor ID does not exist';
        -- Handle any other unexpected database errors
        WHEN OTHERS THEN
            RETURN 'ERROR: Unexpected error';
    END Check_Donor_Eligibility;

    -- Implementation of Process_Lab_Test procedure
    PROCEDURE Process_Lab_Test(
        p_barcode_id IN VARCHAR2,
        p_hiv IN VARCHAR2,
        p_hep_b IN VARCHAR2,
        p_hep_c IN VARCHAR2,
        p_syphilis IN VARCHAR2
    ) IS
        v_overall_safety VARCHAR2(10) := 'Safe';
        v_new_status VARCHAR2(20) := 'Available';
        v_exists NUMBER;
    BEGIN
        -- Check if the blood unit barcode exists in the database
        SELECT COUNT(*) INTO v_exists FROM Blood_Units WHERE Unit_Barcode_ID = p_barcode_id;
        IF v_exists = 0 THEN
            RAISE_APPLICATION_ERROR(-20001, 'The provided Blood Unit Barcode ID does not exist.');
        END IF;

        -- Determine if the unit is Safe or Unsafe based on lab results
        IF p_hiv = 'Positive' OR p_hep_b = 'Positive' OR p_hep_c = 'Positive' OR p_syphilis = 'Positive' THEN
            v_overall_safety := 'Unsafe';
            v_new_status := 'Discarded';
        END IF;

        -- Record the lab test results in Lab_Tests table
        INSERT INTO Lab_Tests (Unit_Barcode_ID, HIV_Result, Hepatitis_B_Result, Hepatitis_C_Result, Syphilis_Result, Test_Date, Overall_Safety)
        VALUES (p_barcode_id, p_hiv, p_hep_b, p_hep_c, p_syphilis, SYSDATE, v_overall_safety);

        -- Update the status of the blood bag in Blood_Units table
        UPDATE Blood_Units SET Status = v_new_status WHERE Unit_Barcode_ID = p_barcode_id;

        -- Commit transaction to apply permanent changes (Transaction Control)
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Success: Lab test processed. Unit status: ' || v_new_status);
    EXCEPTION
        -- Rollback changes if any error occurs during the execution to maintain data consistency
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END Process_Lab_Test;

END BLOOD_BANK_PKG;
/
