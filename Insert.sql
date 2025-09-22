INSERT INTO user (name, email, phone, password)
VALUES 
('Alice Dupont', 'alice.dupont@example.com', '0601020304', 'password1'),
('Bob Martin', 'bob.martin@example.com', '0605060708', 'password2'),
('Charlie Durand', 'charlie.durand@example.com', NULL, 'password3'),
('Diane Leroy', 'diane.leroy@example.com', '0611121314', 'password4');

INSERT INTO book (title, author, genre, publication_date)
VALUES 
('1984', 'George Orwell', 'Dystopie', '1949-06-08'),
('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', '1943-04-06'),
('Harry Potter à l''école des sorciers', 'J.K. Rowling', 'Fantasy', '1997-06-26'),
('Les Misérables', 'Victor Hugo', 'Classique', '1862-01-01'),
('L''Étranger', 'Albert Camus', 'Philosophie', '1942-05-19');

INSERT INTO loan (user_id, book_id, loan_date, return_date, status)
VALUES
(1, 1, '2025-09-01 10:00:00', '2025-09-10 15:00:00', FALSE),  
(2, 2, '2025-09-15 09:30:00', NULL, TRUE),                     
(3, 3, '2025-09-18 14:00:00', NULL, TRUE),                     
(4, 4, '2025-09-10 11:45:00', '2025-09-20 16:30:00', FALSE);  
