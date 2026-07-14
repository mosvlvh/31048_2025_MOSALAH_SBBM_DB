-- =============================================================================
-- FILE: EXPLICIT_CURSOR_TEST.sql
-- DESCRIPTION: Independent script to demonstrate Explicit Cursor requirement
-- =============================================================================

SET SERVEROUTPUT ON;

DECLARE
    -- 1. Declare the Explicit Cursor to fetch discarded blood units
    CURSOR c_unsafe_units IS
        SELECT Unit_Barcode_ID, Blood_Group, Status
        FROM Blood_Units
        WHERE Status = 'Discarded';

    -- Variables to store fetched record values
    v_barcode   Blood_Units.Unit_Barcode_ID%TYPE;
    v_bg        Blood_Units.Blood_Group%TYPE;
    v_status    Blood_Units.Status%TYPE;
    v_counter   NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('==================================================');
    DBMS_OUTPUT.PUT_LINE('   STARTING EXPLICIT CURSOR: UNSAFE BLOOD UNITS   ');
    DBMS_OUTPUT.PUT_LINE('==================================================');

    -- 2. Open the Explicit Cursor
    OPEN c_unsafe_units;

    LOOP
        -- 3. Fetch rows one by one from the active set
        FETCH c_unsafe_units INTO v_barcode, v_bg, v_status;

        -- Exit loop when no more data is found
        EXIT WHEN c_unsafe_units%NOTFOUND;

        -- Process and display the fetched data
        v_counter := v_counter + 1;
        DBMS_OUTPUT.PUT_LINE('Unsafe Unit #' || v_counter || ' -> Barcode: ' || v_barcode || ' | Group: ' || v_bg || ' | Status: ' || v_status);

    END LOOP;

    -- 4. Close the Explicit Cursor to release system resources
    CLOSE c_unsafe_units;

    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Total Discarded/Unsafe Blood Bags Found: ' || v_counter);
    DBMS_OUTPUT.PUT_LINE('==================================================');

EXCEPTION
    -- Safe Exception Handling to ensure cursor closure on unexpected failure
    WHEN OTHERS THEN
        IF c_unsafe_units%ISOPEN THEN
            CLOSE c_unsafe_units;
        END IF;
        DBMS_OUTPUT.PUT_LINE('An error occurred during Cursor execution.');
END;
/
