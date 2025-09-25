TRUNCATE TABLE "loan", "user", "book" RESTART IDENTITY CASCADE;

INSERT INTO "user" (name, email, phone, password, role)
VALUES 
('Alice Dupont', 'alice.dupont@example.com', '0601020304', '$2b$12$xoOTQ3JrOTRG7RZ786fb1OfM0PEi6/AO4NSBZ919tV5pP1zZKhox.', 'user'), -- password: password1
('Bob Martin', 'bob.martin@example.com', '0605060708', '$2b$12$ebtkMnt3isuH5lJQolxLwuc8GQ78SI8bLSxhUPqJxartGSKWH6WR2', 'user'), -- password: password2
('Charlie Durand', 'charlie.durand@example.com', NULL, '$2b$12$4t6YGybq7Z1vJb0QTHc8OOt0kFwn54HZuzZHjcA.AF089/rUd5xdW', 'user'), -- password: password3
('Diane Leroy', 'diane.leroy@example.com', '0611121314', '$2b$12$aox4qAxc5iMPVd/nNHHXquiXwosc92QIbhxl14u3Dygz6CDVCBjca', 'user'), -- password: password4
('Admin', 'admin@example.com', '0612456310', '$2b$12$7MScXRhnZA/lYbmPwnXNaOLtXcIkqVYutqA2xkYBjFCl8jCRFRXXy', 'admin'); -- password: admin

INSERT INTO book (id, title, author, genre, publication_date)
VALUES 
(1, '1984', 'George Orwell', 'Dystopie', '1949-06-08'),
(2, 'Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', '1943-04-06'),
(3, 'Harry Potter à l''école des sorciers', 'J.K. Rowling', 'Fantasy', '1997-06-26'),
(4, 'Les Misérables', 'Victor Hugo', 'Classique', '1862-01-01'),
(5, 'L''Étranger', 'Albert Camus', 'Philosophie', '1942-05-19');

INSERT INTO loan (user_id, book_id, loan_date, return_date, status)
VALUES
(1, 1, '2025-09-01 10:00:00', '2025-09-10 15:00:00', FALSE),  
(2, 2, '2025-09-15 09:30:00', NULL, TRUE),                     
(3, 3, '2025-09-18 14:00:00', NULL, TRUE),                     
(4, 4, '2025-09-10 11:45:00', '2025-09-20 16:30:00', FALSE);