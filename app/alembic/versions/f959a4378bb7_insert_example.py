"""insert_example

Revision ID: f959a4378bb7
Revises: ae522cefad04
Create Date: 2024-11-12 22:39:26.021231

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f959a4378bb7'
down_revision = '71e472659dad'
branch_labels = None
depends_on = None


def upgrade():

    # Inserting dummy data into the 'user' table
    op.execute(
        """
        INSERT INTO "user" (id, name, surname, email, type) VALUES
        (1, 'Alice', 'Johnson', 'alice.johnson@example.com', 'STUDENT'),
        (2, 'Bob', 'Smith', 'bob.smith@example.com', 'PROFESSOR'),
        (3, 'Charlie', 'Brown', 'charlie.brown@example.com', 'OPERATOR'),
        (4, 'Diana', 'Moore', 'diana.moore@example.com', 'ADMIN');
        """
    )
    
    # Inserting dummy data into the 'group' table
    # op.execute(
    #     """
    #     INSERT INTO "group" (id, name, topic, description, created_at, type, owner_id) VALUES
    #     (1, 'Math 101', 'Mathematics', 'Introduction to basic mathematics', current_timestamp, 'public_open', 2),
    #     (2, 'Computer Science Basics', 'Computer Science', 'A beginners guide to computer science', current_timestamp, 'public_closed', 2),
    #     (3, 'Physics 201', 'Physics', 'Advanced topics in physics', current_timestamp, 'private', 1),
    #     (4, 'Web Development', 'Programming', 'Learn how to build websites', current_timestamp, 'public_open', 3),
    #     (5, 'Data Science for Beginners', 'Data Science', 'Introduction to data science concepts', current_timestamp, 'public_open', 2),
    #     (6, 'Advanced Machine Learning', 'Machine Learning', 'Deep dive into ML algorithms', current_timestamp, 'public_closed', 2),
    #     (7, 'Artificial Intelligence Basics', 'AI', 'Learn the foundations of AI', current_timestamp, 'public_open', 1),
    #     (8, 'Ethics in Technology', 'Ethics', 'Discuss ethical issues in modern tech', current_timestamp, 'public_open', 3),
    #     (9, 'Advanced Physics', 'Physics', 'Explore the complexities of quantum mechanics', current_timestamp, 'private', 4),
    #     (10, 'Full-Stack Web Development', 'Programming', 'Build modern web applications from front-end to back-end', current_timestamp, 'public_open', 3),
    #     (11, 'Mobile App Development', 'Programming', 'Creating Android and iOS applications', current_timestamp, 'public_open', 4),
    #     (12, 'Cloud Computing Fundamentals', 'Cloud Computing', 'Learn the basics of cloud infrastructure', current_timestamp, 'public_closed', 2),
    #     (13, 'Data Visualization with Python', 'Data Science', 'Learn to visualize data with Python', current_timestamp, 'public_open', 1),
    #     (14, 'Introduction to Blockchain', 'Blockchain', 'Learn the basics of blockchain and cryptocurrencies', current_timestamp, 'private', 4),
    #     (15, 'Robotics Engineering', 'Robotics', 'Learn how to design and build robots', current_timestamp, 'public_open', 3),
    #     (16, 'Software Engineering Principles', 'Software Engineering', 'Understanding the fundamentals of software engineering', current_timestamp, 'public_closed', 2),
    #     (17, 'Digital Marketing 101', 'Marketing', 'Introduction to digital marketing strategies', current_timestamp, 'public_open', 1),
    #     (18, 'Quantum Computing', 'Quantum Computing', 'Explore the world of quantum computing', current_timestamp, 'private', 2),
    #     (19, 'Cybersecurity Fundamentals', 'Cybersecurity', 'Basic principles of securing computer systems', current_timestamp, 'public_open', 1),
    #     (20, 'Game Development', 'Game Development', 'Learn how to create video games', current_timestamp, 'public_closed', 3),
    #     (21, 'Network Security', 'Cybersecurity', 'Protect networks from cyber threats', current_timestamp, 'public_open', 4),
    #     (22, 'Digital Transformation in Business', 'Business', 'Learn how businesses can adapt to the digital world', current_timestamp, 'public_closed', 1),
    #     (23, 'Data Analytics with R', 'Data Science', 'Learn data analytics with the R programming language', current_timestamp, 'public_open', 2),
    #     (24, 'Introduction to Graphic Design', 'Design', 'Learn the fundamentals of graphic design', current_timestamp, 'public_open', 4),
    #     (25, 'Cloud Application Development', 'Cloud Computing', 'Learn how to develop apps for the cloud', current_timestamp, 'public_open', 3),
    #     (26, 'Web Security and Pen Testing', 'Cybersecurity', 'Learn ethical hacking and web security', current_timestamp, 'private', 2),
    #     (27, 'Artificial Neural Networks', 'AI', 'In-depth study of neural networks', current_timestamp, 'public_closed', 1),
    #     (28, 'IoT (Internet of Things)', 'IoT', 'Learn how devices communicate over the internet', current_timestamp, 'public_open', 3),
    #     (29, 'Advanced SQL and Database Design', 'Databases', 'Master SQL and database architecture', current_timestamp, 'public_open', 2),
    #     (30, 'Cloud Data Engineering', 'Cloud Computing', 'Learn how to build data pipelines in the cloud', current_timestamp, 'private', 4);
    #     """
    #     )

def downgrade():
    # Deleting all records from the 'group' table
    op.execute("""TRUNCATE TABLE "group";""")

    # Deleting all records from the 'user' table
    op.execute("""TRUNCATE TABLE "user"";""")

