-- Project-local Neovim config. Loaded when 'exrc' is set; Neovim asks you to :trust it once.

-- :Snack My Note  -> runs `make snack TITLE="My Note"` and opens the new file
vim.api.nvim_create_user_command("Snack", function(opts)
	local out = vim.fn.system({ "make", "-s", "snack", "TITLE=" .. opts.args })
	if vim.v.shell_error ~= 0 then
		vim.notify(vim.trim(out), vim.log.levels.ERROR)
		return
	end
	local file = vim.trim(out):match("Created (.+)$")
	vim.cmd.edit(vim.fn.fnameescape(file))
	vim.cmd("normal! G")
end, { nargs = "+", desc = "Create a snack and open it" })
