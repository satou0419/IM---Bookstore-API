--CREATE DATABASE
CREATE database dbbook;


--CREATE PROCEDURES
DELIMITER //
CREATE PROCEDURE AddBookProcedure(
    IN new_title VARCHAR(255),
    IN new_author VARCHAR(100),
    IN new_price FLOAT,
    IN new_category_name VARCHAR(255)
)
BEGIN
    DECLARE new_category_id INT;

    -- Check if the category already exists
    SELECT CategoryID INTO new_category_id
    FROM Category
    WHERE CategoryName = new_category_name;

    -- If the category doesn't exist, create a new one
    IF new_category_id IS NULL THEN
        INSERT INTO Category (CategoryName) VALUES (new_category_name);
        SET new_category_id = LAST_INSERT_ID();
    END IF;

    -- Add the book
    INSERT INTO Book (Title, Author, Price, CategoryID)
    VALUES (new_title, new_author, new_price, new_category_id);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE UpdateBookProcedure(
    IN book_id INT,
    IN new_title VARCHAR(255),
    IN new_author VARCHAR(100),
    IN new_price FLOAT,
    IN new_category_name VARCHAR(255)
)
BEGIN
    DECLARE new_category_id INT;

    -- Get the CategoryID for the new_category_name
    SELECT CategoryID INTO new_category_id
    FROM Category
    WHERE CategoryName = new_category_name;

    -- If the category doesn't exist, create it
    IF new_category_id IS NULL THEN
        INSERT INTO Category (CategoryName) VALUES (new_category_name);
        SET new_category_id = LAST_INSERT_ID();
    END IF;

    -- Update the Book
    UPDATE Book
    SET Title = new_title, Author = new_author, Price = new_price, CategoryID = new_category_id
    WHERE BookID = book_id;
END //
DELIMITER;

DELIMITER //
CREATE PROCEDURE DeleteBookProcedure(IN book_id INT)
BEGIN
    -- Declare variables if needed
    DECLARE book_exists INT;

    -- Check if the book exists
    SELECT COUNT(*) INTO book_exists FROM Book WHERE BookID = book_id;

    IF book_exists > 0 THEN
        -- Delete the book
        DELETE FROM Book WHERE BookID = book_id;

        -- Commit the transaction
        COMMIT;
    ELSE
        -- Raise an error or handle as needed
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book does not exist';
    END IF;
END //
DELIMITER 

DELIMITER //
CREATE PROCEDURE AddCategoryProcedure(
    IN new_category_name VARCHAR(255)
)
BEGIN
    DECLARE new_category_id INT;

    -- Check if the category already exists
    SELECT CategoryID INTO new_category_id
    FROM Category
    WHERE CategoryName = new_category_name;

    IF new_category_id IS NULL THEN
        -- Create a new category
        INSERT INTO Category (CategoryName) VALUES (new_category_name);
    END IF;
END //

DELIMITER ;



--CREATE TRIGGER
DELIMITER //
CREATE TRIGGER Book_AfterInsert
AFTER INSERT ON Book
FOR EACH ROW
BEGIN
    INSERT INTO Audit (Action, ObjectType, ObjectID, Timestamp)
    VALUES ('Add', 'Book', NEW.BookID, CURRENT_TIMESTAMP);
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER after_update_book
AFTER UPDATE ON Book
FOR EACH ROW
BEGIN
    DECLARE action_type VARCHAR(255);

    -- Determine the action type based on changes
    IF NEW.Title != OLD.Title OR NEW.Author != OLD.Author OR NEW.Price != OLD.Price OR NEW.CategoryID != OLD.CategoryID THEN
        SET action_type = 'Update';
    END IF;

    -- Insert the audit record if there is a change
    IF action_type IS NOT NULL THEN
        INSERT INTO Audit (Action, ObjectType, ObjectID, Timestamp)
        VALUES (action_type, 'Book', NEW.BookID, CURRENT_TIMESTAMP);
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER DeleteBookTrigger
AFTER DELETE ON Book
FOR EACH ROW
BEGIN
    -- Insert into Audit table with timestamp
    INSERT INTO Audit (Action, ObjectType, ObjectID, Timestamp)
    VALUES ('Delete', 'Book', OLD.BookID, NOW());
END //

DELIMITER ;


DELIMITER //
CREATE TRIGGER category_after_insert
AFTER INSERT ON Category
FOR EACH ROW
BEGIN
    INSERT INTO Audit (Action, ObjectType, ObjectID, Timestamp)
    VALUES ('Add', 'Category', NEW.CategoryID, CURRENT_TIMESTAMP);
END //
DELIMITER ;



--CREATE VIEWS
CREATE VIEW BookView AS
SELECT
    b.BookID,
    b.Title,
    b.Author,
    b.Price,
    c.CategoryName,
    a.Action,
    a.Timestamp
FROM
    Book b
JOIN
    Category c ON b.CategoryID = c.CategoryID
JOIN
    Audit a ON a.ObjectType = 'Book' AND a.ObjectID = b.BookID;


CREATE VIEW vw_category_stats AS
SELECT
    category.CategoryName,
    COUNT(book.BookID) AS TotalBooks,
    MAX(audit.Timestamp) AS CreationDate
FROM
    category
    LEFT JOIN book ON category.CategoryID = book.CategoryID
    LEFT JOIN audit ON category.CategoryID = audit.ObjectID
WHERE
    audit.ObjectType = 'Category'  -- Filter by category-related entries
GROUP BY
    category.CategoryID;
    


CREATE VIEW `vw_audit_logs` AS
    SELECT 
        `audit`.`AuditID` AS `ID`,
        `audit`.`Action` AS `Message`,
        `audit`.`ObjectType` AS `Object Type`,
        `audit`.`ObjectID` AS `Object ID`,
        `audit`.`Timestamp` AS `Date`
    FROM
        `audit`



