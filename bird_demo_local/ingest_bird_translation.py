def _read_csv_duckdb(
    items: Iterator[FileItemDict],
    chunk_size: Optional[int] = 5000,
    use_pyarrow: bool = False,
    **duckdb_kwargs: Any
) -> Iterator[TDataItems]:
    """A resource to extract data from the given CSV files.

    Uses DuckDB engine to import and cast CSV data.

    Args:
        items (Iterator[FileItemDict]): CSV files to read.
        chunk_size (Optional[int]):
            The number of rows to read at once. Defaults to 5000.
        use_pyarrow (bool):
            Whether to use `pyarrow` to read the data and designate
            data schema. If set to False (by default), JSON is used.
        duckdb_kwargs (Dict):
            Additional keyword arguments to pass to the `read_csv()`.

    Returns:
        Iterable[TDataItem]: Data items, read from the given CSV files.
    """
    import duckdb

    helper = fetch_arrow if use_pyarrow else fetch_json

    for item in items:
        with item.open() as f:
            file_data = duckdb.from_csv_auto(f, **duckdb_kwargs)  # type: ignore

            yield from helper(file_data, chunk_size)





def read_csv_with_duckdb() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="standard_filesystem",
        destination='duckdb',
        dataset_name="translation_table",
    )

    # load all the CSV data, excluding headers
    met_files = readers(
        bucket_url="Users/seanmcfall/bird-demo-local/input_data/translation_table/", file_glob="*.csv"
    ).read_csv_duckdb(chunk_size=1000, header=True)

    load_info = pipeline.run(met_files)

    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


