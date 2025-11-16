<?php

declare(strict_types=1);
namespace Src\Groups\App\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Src\Groups\Domain\Dtos\MessageDto;
use Src\Users\Domain\Models\User;

class WriteMessageRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'user_id' => ['required', 'integer', Rule::exists('users', 'id')],
            'group_id' => ['required', 'integer', Rule::exists('groups', 'id')],
            'content' => ['required', 'string'],
        ];
    }

    public function toDto(): MessageDto
    {
        $user = User::find($this->integer('user_id'));

        return new MessageDto(
            user: $user,
            group: $user->groups()->with(['thread.messages'])->get()->where('id', $this->integer('group_id'))->first(),
            content: trim($this->string('content')->toString()),
        );
    }
}
