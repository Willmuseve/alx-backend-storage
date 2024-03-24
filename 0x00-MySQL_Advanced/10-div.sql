-- A SQL script that Creates a function SafeDiv that divides the 1st by the 2nd
-- number or returns 0 if the 2nd number is 0
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
	DECLARE result FLOAT DEFAULT 0;

	IF b != 0 THEN
		SET result = a / b;
	END IF;
	RETURN result;
END $$
DELIMITER ;
