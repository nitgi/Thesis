import pandas as pd
import random


# Set the seed for reproducibility
random.seed(10)


def select_canonical(dataframe):
    # Sort the DataFrame by 'canonicity' column in descending order
    sorted_df = dataframe.sort_values(by='DBNLSecRefsTitle', ascending=False)

    # Initialize an empty list to store selected rows
    selected_books = []

    # Iterate over the sorted DataFrame
    for _, row in sorted_df.iterrows():
        # Check if the author of the current row is already selected
        if row['Author'] not in [book['Author'] for book in selected_books]:
            # Append the current row to the selected_books list
            selected_books.append(row)

            # Check if 20 rows are already selected
            if len(selected_books) == 22:
                break

    # Return selected books as DataFrame
    return pd.DataFrame(selected_books)


def select_non_canonical(dataframe):
    # Get the unique authors in the filtered DataFrame
    unique_authors = dataframe['Author'].unique()

    # Randomly select 20 unique authors
    selected_authors = random.sample(list(unique_authors), 20)

    # Create an empty DataFrame to store the selected books
    selected_df = pd.DataFrame(columns=dataframe.columns)

    # Iterate over the selected authors and select the first book by each author
    for author in selected_authors:
        author_books = dataframe[dataframe['Author'] == author]
        first_book = author_books.iloc[0]
        selected_df = selected_df.append(first_book)

    # Return selected books as DataFrame
    return selected_df


def main():
    df = pd.read_csv('metadata.tsv', sep='\t')

    # Select the books in the desired range of years (where genre is proza)
    filtered_years = df[(df['YearFirstPublished'] >= 1850)
                        & (df['YearFirstPublished'] <= 1950)
                        & (df['DBNLgenre'] == 'proza')]

    # Select the non-canonical books
    non_canonical = filtered_years[filtered_years['DBNLSecRefsTitle'] == 0]

    # Select the canonical books
    canonical = filtered_years[filtered_years['DBNLSecRefsTitle'] != 0]

    filtered_non_canonical = select_non_canonical(non_canonical)
    filtered_canonical = select_canonical(canonical)

    print(filtered_canonical)
    print('\n\n\n\n')
    print(filtered_non_canonical)


if __name__ == '__main__':
    main()
